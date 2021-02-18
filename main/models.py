
"""
NAME
    models.py

DESCRIPTION
    Contains the models for the game settings, the playing card, and the game contents along with the
    methods to interact with them.

CLASS
    GameSettings                   -- stores the settings for a particular game (current wild card,
                                      current card deck, list of players, each player's cards, the
                                      discard pile, items displayed on the game board, the number of
                                      jokers, the active player, and the current dealer)
    Card                           -- defines a playing card: the suit and face value (Note:
                                      jokers have a suit of 'joker' and face value of 'joker')
    Games                          -- stores all the currently active games

METHODS
                        GameSettings Class
    __init__                       -- initializes the settings for a particular game
    __str__                        -- formatted string to print out some of settings (used for testing)
    reset_game                     -- clears each player's hand in the game
    add_selections                 -- add user selections to the object (number of jokers)
    get_wild_card                  -- getter - get the current wild card value
    set_wild_card                  -- setter - set the current wild card value
    get_players                    -- get the list of players in the game
    get_top_card                   -- get the top card from the card deck
    append_card                    -- append a card to the card deck (when building the deck)
    get_players_cards              -- get a list of all the players' cards (dictionary style)
    get_player_cards               -- get a list of a particular player's cards
    get_discards                   -- get a list of the cards in the discard pile
    get_game_board_items           -- get all the card melds and types of melds (book or run) from game board
    add_player                     -- add a player to the player list for a game
    add_player_cards               -- add cards to a selected player's hand
    del_player_cards               -- delete a card from a player's hand
    add_discards                   -- add a card to the discard pile
    del_discards                   -- delete the cards in the discard pile
    add_game_board_items           -- add a card meld and type (book or run) to the game board
    del_game_board_items           -- delete the contents of the game board (new game or new deal)
    remove_player                  -- remove a player from the game
    set_active_player              -- setter - set the active player - it's their turn now
    get_active_player              -- getter - get the active player's name
    set_dealer                     -- setter - set the dealer's name
    get_dealer                     -- getter - get the current dealer's name
                        Card Class
    __init__                       -- initialize a card's value - suit and face value
    __gt__                         -- used to determine card order (used durirng testing)
    __str__                        -- used to print formatted string of card value (used during testing)
                        Games Class
    __init__                       -- initializes the games dictionary accessible by game_id
    __str__                        -- used to print all games contents (used during testing)
    add_game                       -- adds a new game using the specified game_id
    add_player                     -- adds a player to an existing game using the player name and game_id
    pop_top_card                   -- obtains the top card from the deck of cards for the selected game_id
    clear_deck                     -- clears the deck for the specified game
    append_card                    -- appends a card (suit, face value) to the deck for the specified game_id
    get_wild_card                  -- getter - get the current wild card value
    set_wild_card                  -- setter - sets the current wild card value
    add_player_cards               -- add card to a specified player's hand for the specified game_id
    del_player_cards               -- delete the hand of cards for the specified player for the specified game_id
    add_discards                   -- add card to the discard pile for the specified game_id
    del_discards                   -- delete all the cards from the discard pile for the specified game_id
    add_game_board_items           -- add a card_meld and type (book or run) to the game board
                                      for the specified game_id
    del_game_board_items           -- delete all the items on the game board for the specified game_id
    get_players                    -- getter - get the list of players for the specified game_id
    get_player_cards               -- getter - get the list of cards held by the specified player
                                      for the specified game_id
    get_discards                   -- getter - get the list of cards in the discard pile for the specified game_id
    get_game_board_items           -- getter - get the list of game board items for the specified game_id
                                      including meld_cards (the cards played on the board) and the type
                                      of meld (book-matching face value, run-same suit in consecutive order)
    get_game                       -- getter - get the game contents for the specified game_id
    get_deck                       -- getter - get the deck for the specified game_id
    shuffle                        -- randomize the cards in the deck for the specified game_id
    set_active_player              -- setter - set the active player for the specified game_id
    get_active_player              -- getter - get the active player for the specified game_id, it is their turn
    set_dealer                     -- setter - set the current dealer for the specified game_id
    get_dealer                     -- getter - get the current dealer for the specified game_id
    remove_player                  -- remove a player from the player list for a specified game_id
    remove_game                    -- remove a game from the dictionary of games for the specified game_id
    print_game                     -- print the contents of the game for the specified game_id

DATA
    games                          -- contains any active game data (settings, players, cards, ...)
"""

import random

all_suits = ['spades', 'clubs', 'hearts', 'diamonds']
all_facevals = ['2','3','4','5','6','7','8','9','10','J','Q','K', 'A']


# Contains all the settings for a particular game play
class GameSettings:
    def __init__(self):
        self.wild_card = ""         # current wild card face value
        self.deck = []              # the list of cards in the game's deck
        self.players = []           # the list of players
        self.player_cards = {}      # the list of cards for each player
        self.discards = []          # the list of cards in the discard pile
        self.game_board_items = []  # the list of card melds and type on the game board
        self.number_of_jokers = 0   # the number of jokers in the game
        self.active_player = ""     # the name of the active player
        self.dealer = ""            # the name of the player that dealt the cards

    def __str__(self):
        return_string = "Deck Size="+str(len(self.deck)) + "\n"
        return_string += "players="+str(self.players) + "\n"
        return_string += "Number of jokers="+str(self.number_of_jokers) + "\n"
        return return_string

    # clear the cards in each player's hand
    def reset_game(self):
        for player in self.player_cards:
            self.player_cards[player] = []

    # add user selections to the game (currently only the number of jokers in the deck)
    def add_selections(self, number_of_jokers):
        self.number_of_jokers = number_of_jokers

    # getter - return the current wild card
    def get_wild_card(self):
        return self.wild_card

    # setter - set the current wild card
    def set_wild_card(self, wild_card):
        self.wild_card = wild_card

    # getter - return the list of players
    def get_players(self):
        return self.players

    # return the top card from the card deck
    def get_top_card(self):
        return self.deck.pop(0)

    # append a card to the card deck
    def append_card(self, card):
        self.deck.append(card)

    # getter - get the list of cards for each player
    def get_players_cards(self):
        return self.player_cards

    # getter - get the list of cards for a specified player
    def get_player_cards(self, user_name):
        return self.player_cards[user_name]

    # getter - get the list of cards in the discard pile
    def get_discards(self):
        return self.discards

    # getter - get the card melds and types that were played on the game board
    def get_game_board_items(self):
        return self.game_board_items

    # add a player to the game
    def add_player(self, player):
        self.players.append(player)
        self.player_cards[player] = []

    # add a card for a specified player in the game
    def add_player_cards(self, player, card):
        self.player_cards[player].append(card)

    # delete the list of cards for the specified player
    def del_player_cards(self, player):
        del self.player_cards[player]
        self.player_cards[player] = []

    # add a card to the list of cards in the discard pile
    def add_discards(self, card):
        self.discards.append(card)

    # delete all cards from the discard pile
    def del_discards(self):
        del self.discards
        self.discards = []

    # add  the card meld and type (run or book) to the game board
    def add_game_board_items(self, type, meld_cards):
        self.game_board_items.append({"type": type, "meld_cards": meld_cards})

    # delete all the game board items
    def del_game_board_items(self):
        del self.game_board_items
        self.game_board_items = []

    # remove a player from the game
    def remove_player(self, user_name):
        self.players.remove(user_name)

    # setter - set the active player to the specified user
    def set_active_player(self, user_name):
        self.active_player = user_name

    # getter - get the active player's name
    def get_active_player(self):
        return self.active_player

    # setter - set the game's dealer to the specified name
    def set_dealer(self, dealer):
        self.dealer = dealer

    # getter - get the name of the current dealer
    def get_dealer(self):
        return self.dealer


# contains the suit and face value for a particular card object
class Card:
    # initialize the suit and face value for the card
    def __init__(self, suit, faceval):
        self.suit = suit
        self.faceval = faceval

    # compare a card to another card (used during testing)
    def __gt__(self, other):
        if self.suit != other.suit:
            # put jokers at the end
            if self.suit == 'joker':
                return True
            elif other.suit == 'joker':
                return False
            return self.suit > other.suit
        else:
            return self.faceval > other.faceval

    # create custom string for printing (used during testing)
    def __str__(self):
        return self.faceval + " of " + self.suit


# contains all the active games in play
class Games:
    # Initialize the game dictionary - games accessed by game id selected by the users
    def __init__(self):
        self.games = {}

    # create custom string for printing all game contents (used during testing)
    def __str__(self):
        return_string = ""
        for game in self.games:
            return_string += str(self.games[game])
            return_string += "\n"
        return return_string

    # add a new game to the game object including: number_of_jokers and number_of decks
    def add_game(self, game_id, number_of_jokers, number_of_decks):
        deck = []
        self.games[game_id] = GameSettings()
        # add the selected number of decks to the game deck
        for deck_ctr in range(0,int(number_of_decks)):
            # add each card (2,...10, J, Q,K, A) to the game deck
            for suit in all_suits:
                for faceval in all_facevals:
                    card = Card(suit, faceval)
                    deck.append(card)
        if number_of_jokers is None:
            number_of_jokers = 2
        # add the selected number of jokers to the game deck
        for i in range(0, number_of_jokers):
            card = Card('joker', '?')
            deck.append(card)
        self.games[game_id].deck = deck
        self.games[game_id].add_selections(number_of_jokers)

    # add the specified player for the specified game_id
    def add_player(self, game_id, player):
        players = self.games[game_id].get_players()
        #
        if player not in players:
            self.games[game_id].add_player(player)

    # get the top card from the specified game's deck based on game_id
    def pop_top_card(self, game_id):
        return self.games[game_id].get_top_card()

    # clear the deck for the specified game_id
    def clear_deck(self, game_id):
        self.games[game_id].deck = []

    # append a card (suit, face value) to the deck for the specified game_id
    def append_card(self, game_id, suit, faceval):
        card = Card(suit, faceval)
        self.games[game_id].append_card(card)

    # get the current wild card for the specified game_id
    def get_wild_card(self, game_id):
        return self.games[game_id].get_wild_card()

    # set the current wild card for the specified game_id
    def set_wild_card(self, game_id, wild_card):
        self.games[game_id].set_wild_card(wild_card)

    # add a card to a player's hand for the specified player for the specified game_id
    def add_player_cards(self, game_id, player, card):
        if game_id in self.games.keys():
            players_cards = self.games[game_id].get_players_cards()
            if player in players_cards.keys():
                self.games[game_id].add_player_cards(player, card)

    # delete all cards for the specified player for the specified game_id
    def del_player_cards(self, game_id, player):
        self.games[game_id].del_player_cards(player)

    # add a card (suit, face value) to the discard pile for the specified game_id
    def add_discards(self, game_id, card):
        if game_id in self.games.keys():
            self.games[game_id].add_discards(card)

    # delete all cards from the discard pile for the specified game_id
    def del_discards(self, game_id):
        self.games[game_id].del_discards()

    # add cards and meld type (run or book) to the game board for the specified game_id
    def add_game_board_items(self, game_id, meld_type, meld_cards):
        if game_id in self.games.keys():
            self.games[game_id].add_game_board_items(meld_type, meld_cards)

    # delete all game board items for the specified game_id
    def del_game_board_items(self, game_id):
        self.games[game_id].del_game_board_items()

    # getter - get the list of players for the specified game_id
    def get_players(self, game_id):
        if game_id in self.games.keys():
            return self.games[game_id].players
        else:
            return None

    # getter - get the list of cards for the specified player for the specified game_id
    def get_player_cards(self, game_id, user_name):
        if game_id in self.games.keys():
            players_cards = self.games[game_id].get_players_cards()
            if user_name in players_cards.keys():
                return self.games[game_id].get_player_cards(user_name)
        return None

    # getter - get the list of cards in the discard pile for the specified game_id
    def get_discards(self, game_id):
        if game_id in self.games.keys():
            return self.games[game_id].get_discards()

    # getter - get the list of items (cards and meld_type-run or book) for the specified game_id
    def get_game_board_items(self, game_id):
        if game_id in self.games.keys():
            return self.games[game_id].get_game_board_items()

    # getter - get the game contents for the specified game_id
    def get_game(self, game_id):
        if game_id in self.games.keys():
            return self.games[game_id]
        else:
            return None

    # getter - get the deck of cards for the specified game_id
    def get_deck(self, game_id):
        if game_id in self.games.keys():
            return self.games[game_id].deck
        else:
            return None

    # randomize the cards in the deck of cards for the specified game_id
    def shuffle(self, game_id):
        if game_id in self.games.keys():
            self.games[game_id].reset_game()
            random.shuffle(self.games[game_id].deck)
            return self.games[game_id].deck
        else:
            return None

    # setter - set the active player in the game for the specified game_id
    def set_active_player(self, game_id, player):
        if game_id in self.games.keys():
            self.games[game_id].set_active_player(player)

    # getter - get the active player in the game for the specified game_id
    def get_active_player(self, game_id):
        if game_id in self.games.keys():
            return self.games[game_id].get_active_player()
        else:
            return None

    # setter - set the dealer's name in the game for the specified game_id
    def set_dealer(self, game_id, dealer):
        if game_id in self.games.keys():
            self.games[game_id].set_dealer(dealer)

    # getter - get the dealer's name in the game for the specified game_id
    def get_dealer(self, game_id):
        if game_id in self.games.keys():
            return self.games[game_id].get_dealer()
        else:
            return None

    # remove a player from the game for the specified game_id
    def remove_player(self, game_id, player):
        if game_id in self.games.keys():
            if player in self.games[game_id].get_players():
                self.games[game_id].remove_player(player)
            if len(self.games[game_id].get_players()) == 0:
                self.remove_game(game_id)

    # remove a game from the game dictionary using the specified game_id
    def remove_game(self, game_id):
        if game_id in self.games.keys():
            del self.games[game_id]

    # print the contents of all the games - used during testing
    def print_game(self, game_id):
        for card in self.games[game_id].deck:
            print(card)
