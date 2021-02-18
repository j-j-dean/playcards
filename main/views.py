"""
NAME
    views.py

DESCRIPTION
    Controls the views displayed to the user, and controls game play objects displayed to players

FUNCTIONS
    stream         /stream/<game_id>/<user>/ - received from each player to establish connection with the player
                                   -- used to setup and use the server sent events (SSE)
                                      protocol with the players in the game.  Game data is streamed to
                                      players through a HTTP streamed response
    homepage       '' (default) - view
                                   -- provides the starting point for the user.  This function creates
                                      the initial view to the user providing the option to create or
                                      join a game.
    create         /create/ - view
                                   -- provides a view that dialogs with the user to create a new game.
    gamepage       /game-page/<game_id>/<user>/ - view
                                   -- generates the game board after a successful creation of a game, or
                                      after successfully joining a game in progress
    join           /join/ - view
                                   -- provides a view that dialogs with the user to join a game in progress.
    deal           /deal/<game_id>/<user> - causes server side event to update each player's game board
                                   -- modifies the game board in response to a deal request by randomly
                                      shuffling the deck of cards and dealing cards to each player
    turncompletepost  /game-page/<game_id>/<user>/turn_complete_post - receives ajax request from player to update game
                                   -- updates the game board for all players after a player's turn is
                                      complete.  During a player's turn the game contents for the active
                                      player is performed in java script.  Only after the turn is complete
                                      are all the player's boards updated.
    show_cards     /show-cards/<game_id>/ - view displaying selected contents of game play (used for testing)
                                   -- displays the contents of the selected game
    exit           /exit/<game_id>/<user>
                                   -- exits a player from the selected game

DATA
    games                          -- contains any active game data (settings, players, cards, ...)
    update_available               -- a threading.Event() is created for each player, and the set(), clear(),
                                      and wait() methods are used to control game board updates to each
                                      player.  A set() is used to indicate an update available for a player.
                                      A clear() is used to indicate the update for the player is complete.
                                      And the wait() is used asynchronously to wait for updates.
    update_type_list               -- contains a list of updates to the game board.  This list is initially
                                      created when a game is created.  And items are appended to the list
                                      when user's are added to the game, when cards are dealt, and when a
                                      player completes their turn.  When an item from the update list has
                                      been updated to all players it is removed from the list.

"""

from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseNotFound, StreamingHttpResponse

from . import models
from .forms import GameSettingsForm, GameJoinForm

import json
import threading
import itertools

BLITZ_DEAL_VALUE_TEN = ['J', 'Q', 'K', 'A', '?']

update_available = {}    # used to perform updates for each player in each game as an asynchronous threading.Event()
update_type_list = {}    # used to maintain a list of updates being performed


# create connection with players in the game through Server Sent Events (SSE)
def stream(request, game_id, user_name):

    # update and store a stream_id for the player creating the connection
    #   (when a refresh occurs on user's screen a new '/stream/' request occurs -
    #    this allows only the active stream_id to be processed)
    if game_id in update_available.keys():
        if user_name in update_available[game_id].keys():
            if hasattr(update_available[game_id][user_name], 'stream_id'):
                update_available[game_id][user_name].stream_id += 1
            else:
                update_available[game_id][user_name].stream_id = 1

    # create the HttpStreamingResponse connection with the player to perform game updates
    def event_stream():

        stream_id = int(update_available[game_id][user_name].stream_id)
        while True:
            # wait until an update is requested - a separate stream will be attached to each player
            update_available[game_id][user_name].wait()

            # check to see if stream_id is the correct one, otherwise break out of the loop -
            #   this will ensure old event streams are cleaned up; if a player refreshes their
            #   screen they invoke a new event_stream, so this will exit the stream for the
            #   stream that no longer is active
            if stream_id != update_available[game_id][user_name].stream_id:
                update_available[game_id][user_name].clear()
                print("(event_stream) This may cause ConnectionAbortedError - maybe fixed in Python 3.8+")
                break  # exit the for loop - this is the old event stream

            # create the updated game data object to send to the player including:
            #   game update type, player's cards, game deck, list of players, dealer, active player,
            #   discard pile, game board contents, count of each player's cards, wild card
            card_counts = []
            players = games.get_players(game_id)
            deck_cards = []
            for card in games.get_deck(game_id):
                new_card = {"suit": card.suit, "faceval": card.faceval}
                deck_cards.append(new_card)
            discards = []
            for card in games.get_discards(game_id):
                new_card = {"suit": card.suit, "faceval": card.faceval}
                discards.append(new_card)
            player_cards = []
            for card in games.get_player_cards(game_id, user_name):
                new_card = {'suit': card.suit, 'faceval': card.faceval}
                player_cards.append(new_card)
            game_board_items = []
            for item in games.get_game_board_items(game_id):
                meld_cards = []
                for meld_card in item['meld_cards']:
                    new_meld_card = {"player":meld_card['player'], "suit":meld_card['suit'], "faceval":meld_card['faceval']}
                    meld_cards.append(new_meld_card)
                game_board_items.append({"type": item['type'], "meld_cards":meld_cards})
            for pndx in range(len(players)):
                card_counts.append(len(games.get_player_cards(game_id, players[pndx])))
            try:
                if update_type_list[game_id][0]['type'] == 'update_game':
                    update_type_list[game_id][0]['players_updated'] += 1
                    data_obj = {
                        'type': 'update_game',
                        'player_cards': player_cards,
                        'deck_cards' : deck_cards,
                        'players': players,
                        'dealer': games.get_dealer(game_id),
                        'active_player': games.get_active_player(game_id),
                        'discards' : discards,
                        'gameboard' : game_board_items,
                        'card_counts': card_counts,
                        'wild_card': games.get_wild_card(game_id),
                    }
                else:
                    data_obj = {'type': 'unknown', }
                    print("(event_stream) unknown DATA OBJECT")

                # remove the update from list of updates when all players have received the update
                if update_type_list[game_id][0]['players_updated'] >= update_type_list[game_id][0]['player_count']:
                    update_type_list[game_id].pop(0)

                # convert the data to JSON format and yield (send) the data to the player
                data_json_string = json.dumps(data_obj)
                yield 'data: '+data_json_string+'\n\n'

            # print message to console if exception occurs (used during testing)
            except:
                print("(event_stream)****************Exception occurred in Stream event")
                print("(event_stream)for id:" + str(stream_id) + " game_id:" + game_id + " and user:" + user_name)
                print("(event_stream)update_type_list[game_id] = " + str(update_type_list[game_id]))

            # clear update_available for the player to wait for future updates
            update_available[game_id][user_name].clear()

    return StreamingHttpResponse(event_stream(), content_type='text/event-stream')


games = models.Games()  # games contains the game model: settings and game contents for each game being played


# '/' homepage is the default view when beginning
def homepage(request):
    return render(request=request, template_name="homepage.html",
                  context={"categories": "future.model.objects.all()"})


# '/create/' create view performs a dialog with the user to create a game
def create(request):

    # POST - verify the user request is valid.  If valid redirect to the game-page view
    if request.method == "POST":
        form = GameSettingsForm(request.POST)
        form.games = games
        if form.is_valid():
            game_id = form.cleaned_data['game_id']
            user_name = form.cleaned_data['user_name']
            if games.get_game(game_id):
                status_msg = "Error: "+game_id+" already in use"
                return render(request,'homepage.html',context={'status_msg':status_msg})
            number_of_jokers = form.cleaned_data['number_of_jokers']
            number_of_decks = form.cleaned_data['number_of_decks']
            games.add_game(game_id, number_of_jokers, number_of_decks)
            games.add_player(game_id, user_name)
            games.set_active_player(game_id, user_name)
            update_available[game_id] = {}
            update_type_list[game_id] = []
            update_available[game_id][user_name] = threading.Event()
            return redirect('game-page', game_id, user_name)
        else:
            return render(request, 'creategamesettings.html', {'form':form})

    # GET - display the dialog form requesting input from the user to create a game
    else:
        form = GameSettingsForm()
        return render(request, 'creategamesettings.html', {'form': form})


# '/game-page/<game_id>/<user>/' game view displaying players, game board, and game play interface
def gamepage(request, game_id, user_name):
    # get the game information and display the following to the game board:
    #   game id, user name, dealer, player's cards, discard pile, wild card, the remaining cards in the deck,
    #   the list of players and the number of cards each player has, active player, game board contents
    cards = []
    for card in games.get_deck(game_id):
        new_card = {"suit": card.suit, "faceval": card.faceval}
        cards.append(new_card)
    deck_json = json.dumps(cards)
    wild_card = games.get_wild_card(game_id)
    user_cards = games.get_player_cards(game_id, user_name)
    discards = games.get_discards(game_id)
    players = games.get_players(game_id)
    players_and_counts = []
    for player in players:
        player_and_count = {
            'name': player,
            'card_count': len(games.get_player_cards(game_id, player)),
        }
        players_and_counts.append(player_and_count)
    active_player = games.get_active_player(game_id)
    dealer = games.get_dealer(game_id)
    game_board_items = games.get_game_board_items(game_id)
    return render(request=request, template_name="gamepage.html",
                  context={'user_name': user_name, 'game_id': game_id, 'dealer': dealer, 'user_cards': user_cards,
                           'discards': discards, 'wild_card': wild_card, 'card_deck': deck_json,
                           'players_and_counts': players_and_counts, 'active_player': active_player,
                           'game_board_items': game_board_items})


# '/join/' join view performs a dialog with the user to join an existing game
def join(request):

    # POST - verify the user request is valid.  If valid redirect to the game-page view
    if request.method == "POST":
        form = GameJoinForm(request.POST)
        form.games = games
        if form.is_valid():
            user_name = form.cleaned_data['user_name']
            game_id = form.cleaned_data['game_id']
            games.add_player(game_id, user_name)
            player_count = len(games.get_players(game_id))
            update_type_list[game_id].append({'type':'update_game', 'player_count': player_count, 'players_updated': 1})
            update_available[game_id][user_name] = threading.Event()
            for player in games.get_players(game_id):
                if player != user_name:
                    update_available[game_id][player].set()

            return redirect('game-page', game_id, user_name)
        else:
            return render(request, "join.html", {'form': form})

    # GET - display the dialog form requesting input from the user to join a game
    else:
        form = GameSettingsForm()
        return render(request, "join.html", {'form': form})


# '/deal/<game_id>/<user>/' the deal action randomizes the cards in the card deck and
#   updates the view for player selecting to deal, the other player's views are then
#   updated asynchronously through server sent events
def deal(request, game_id, user_name):
    # Set the dealer name
    games.set_dealer(game_id, user_name)

    # Set the active player to player after dealer
    players = games.get_players(game_id)
    pndx = 0
    for player in games.get_players(game_id):
        pndx += 1
        if player == user_name:
            break
    if pndx >= len(players):
        pndx = 0
    games.set_active_player(game_id, players[pndx])

    # return all players cards to the deck
    for player in games.get_players(game_id):
        for card in games.get_player_cards(game_id, player):
            games.append_card(game_id, card.suit, card.faceval)
        games.del_player_cards(game_id, player)

    # shuffle the cards
    games.shuffle(game_id)

    # clear the game board
    games.del_game_board_items(game_id)

    # deal cards Blitz style (the first card dealt determines how many cards the player is dealt
    games.set_wild_card(game_id, "")
    for player in games.get_players(game_id):
        next_card = games.pop_top_card(game_id)
        if next_card.faceval in BLITZ_DEAL_VALUE_TEN:  # 10 cards will be dealt for non-numbered cards
            cards_to_deal = 10 - 1
        else:
            cards_to_deal = int(next_card.faceval) - 1  # the numerical value determines the # of cards to deal

        # set the wild card to the dealer's first card (Blitz rules)
        if player == user_name:
            if games.get_wild_card(game_id) == "":
                games.set_wild_card(game_id, next_card.faceval)

        # add cards to the player's hand based on the first card they were dealt
        games.add_player_cards(game_id, player, next_card)
        for i in itertools.repeat(None, cards_to_deal):
            next_card = games.pop_top_card(game_id)
            games.add_player_cards(game_id, player, next_card)

    # clear discard pile and place next card on discard pile
    games.del_discards(game_id)
    next_card = games.pop_top_card(game_id)
    games.add_discards(game_id, next_card)

    # update all users
    player_count = len(games.get_players(game_id))
    update_type_list[game_id].append({'type': 'update_game', 'player_count': player_count, 'players_updated': 1})
    for player in games.get_players(game_id):
        if player != user_name:
            update_available[game_id][player].set()

    return redirect('game-page', game_id, user_name)


# '/game-page/<game_id>/<user>/turn_complete_post' the player has completed their turn
#   and sent back updates to the game board for all players
def turncompletepost(request, game_id, user_name):

    # POST - only expecting this from the player when the turn is complete to update saved game info
    if request.method == 'POST':

        # update the game deck for the specified game
        deck_json = json.loads(request.POST.get('updated_deck'))
        games.clear_deck(game_id)
        for card in deck_json:
            games.append_card(game_id, card['suit'], card['faceval'])

        # update the players hand in the for the specified game
        updated_players_hand = json.loads(request.POST.get('updated_players_hand'))
        games.del_player_cards(game_id, user_name)
        for card in updated_players_hand:
            games.add_player_cards(game_id, user_name, models.Card(card['suit'], card['faceval']))

        # update the saved discard pile for the specified game
        discards = json.loads(request.POST.get('discards'))
        games.del_discards(game_id)
        for card in discards:
            games.add_discards(game_id, models.Card(card['suit'], card['faceval']))

        # update the saved game board contents for the specified game
        game_board = json.loads(request.POST.get('game_board'))
        games.del_game_board_items(game_id)
        for item in game_board:
            item_type = item['type']
            meld_cards = []
            for meld_card in item['meld_cards']:
                print("item-"+item_type+", meld_card="+str(meld_card))
                meld_cards.append({"player":meld_card['player'],
                                   "suit":meld_card['suit'],
                                   "faceval":meld_card['faceval']})
            games.add_game_board_items(game_id, item_type, meld_cards)

        # Update the active player to the next player for the specified game
        active_player_found = False
        new_active_player = games.get_players(game_id)[0] # set new active player to first in list
        for player in games.get_players(game_id):
            if active_player_found:
                new_active_player = player
                break
            if player == user_name:
                active_player_found = True
        games.set_active_player(game_id, new_active_player)

        # Update the player information on all user screens for the specified game
        player_count = len(games.get_players(game_id))
        update_type_list[game_id].append(
            {'type': 'update_game', 'player_count': player_count, 'players_updated': 1})
        for player in games.get_players(game_id):
            if player != user_name:
                print("TurnComplete-update going to "+player)
                update_available[game_id][player].set()

        # the following message is sent in response to ajax call for a success; helpful during testing
        return HttpResponse(
            json.dumps({"working on this": "it's happening"}),
            content_type="application/json"
        )

    # this shouldn't happen; helpful during testing
    else:
        return HttpResponse(
            json.dumps({"nothing to see": "this isn't happening"}),
            content_type="application/json"
        )


# '/show-cards/<game_id>/ shows some of the game contents for the specified game, helpful during testing
def show_cards(request, game_id):

    # create a list of players for the specified game and their cards to display to the view
    player_list = []
    players = games.get_players(game_id)
    if players:
        for player in games.get_players(game_id):
            players_cards = games.get_player_cards(game_id, player)
            player_contents = {
                'name': player,
                'cards': players_cards,
            }
            player_list.append(player_contents)

    # get the game deck for the specified game to display to the view
    deck = games.get_deck(game_id)

    return render(request, "showallcards.html", context={'game_id': game_id,
                           'player_list': player_list, 'deck': deck})


# '/exit/<game_id>/<user>/' removes the player from the game for the specified game
def exit(request, game_id, user_name):
    if games:
        games.remove_player(game_id, user_name)
    return redirect('homepage')

