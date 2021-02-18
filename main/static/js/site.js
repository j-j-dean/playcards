
/*************************************************************************************
*  Next add comments here for JavaScript file!!!!
**************************************************************************************/
var all_suits = ['spades', 'clubs', 'hearts', 'diamonds'];
var all_facevals = ['2','3','4','5','6','7','8','9','10','J','Q','K', 'A'];
var joker_faceval = "?";
var joker_suit = "joker";

var playingCards = {
    my_hand: [],
    discard_pile: [],
    game_board: [],
    wild_card: "",
    max_z_index: 0,
    meld_order: 0,
};

// SVG for back of the card defined here and added after the window loads
var card_svg = '<svg width="100%" height="100%">';
card_svg += '<defs>';
card_svg += '<pattern id="polka-dots" x="0" y="0" width="10%" height="9%" patternUnits="userSpaceOnUse">';
card_svg += '<rect x="1" y="1" width="10" height="14" style="fill:rgb(255,161,161)"></rect>';
card_svg += '<line x1="1" y1="1" x2="11" y2="15" style="stroke:rgb(203,65,84);stroke-width:3" />';
card_svg += '<line x1="11" y1="1" x2="1" y2="15" style="stroke:rgb(203,65,84);stroke-width:3" />';
card_svg += '</pattern>';
card_svg += '</defs>';
card_svg += '<rect x="0" y="0" width="100%" height="100%" fill="url(#polka-dots)"></rect>';
card_svg += '</svg>';

// Get the suit based on the given elements class
playingCards.getSuit = function($elem) {
    if ($elem.hasClass('suithearts')) {
        suit = "hearts";
    } else if ($elem.hasClass('suitclubs')) {
        suit = "clubs";
    } else if ($elem.hasClass('suitspades')) {
        suit = "spades";
    } else if ($elem.hasClass('suitdiamonds')) {
        suit = "diamonds";
    } else { // set to joker if no suit class
        suit = joker_suit;
    }
    return suit;
}

// Perform initializations
playingCards.Initialize = function() {
    // reset status message
    $('#status_msg').text("");
    // store player's hand
    playingCards.StoreMyHand();
    // store discards
    playingCards.StoreDiscards();
    // update game board
    playingCards.StoreGameBoard();
        // make user's hand draggable to allow custom ordering
    playingCards.MakeDraggable();
    // set card value attribute used by css to display card value in corner of cards
    playingCards.AddCardValueAttributes();
    // update the number of cards displayed in the user's hand
    playingCards.UpdateCardCount();
    // update the current wildcard in play
    playingCards.wild_card = $('#wild_card').text().trim().slice("Wild Card ".length).trim();
}

// Reset menu selections when a new menu choice is selected
playingCards.ResetMenuSelections = function() {
    // remove click handlers from the players cards
    $('.players_card').off('click');
    // remove discard class from the players cards (when discard was in progress)
    $('.players_card').removeClass("discard");
    // remove meld_card class and meld_order attribute from the players cards (when play new/add was in progress)
    $('.players_card').removeClass("meld_card");
    $('.players_card').removeAttr("meld_order");
    // remove game board event handlers and card-selected class from all cards on the game board
    $('#game-board>div').each(function() {
        var $game_board_div = $(this);
        $game_board_div.off();
        $game_board_div.find(".card_value").each(function() {
            $(this).parent().removeClass("card-selected");
        });
    });
}

// Make cards being viewed in the player's hand draggable
playingCards.MakeDraggable = function() {
    // Make players cards draggable
    $('.players_card').draggable({
        // Change the order of the cards in the user's hand after a drag action is stopped
        stop: function() {
            // Get the position, suit and faceval of the moved card
            playingCards.max_z_index++;
            var new_position = $(this).position();
            var $drag_card = $(this);
            var card_dropped = false;
            var drag_card_suit = playingCards.getSuit($drag_card);
            var drag_card_faceval = $drag_card.find("p").text().trim();
            $drag_card.css("z-index", playingCards.max_z_index.toString());

            // Move the card before the next card in the user's hand
            $('.players_card').each(function() {
                var position = $(this).position();
                if (!card_dropped) {
                    if (parseInt(position.left) >= parseInt(new_position.left)) {
                        var card_suit = playingCards.getSuit($(this));
                        var faceval = $(this).find("p").text().trim();
                        // skip the card that matches the dragged card
                        if (!(drag_card_suit == card_suit) || !(drag_card_faceval == faceval)) {
                            $drag_card.insertBefore($(this));
                            card_dropped = true;
                        }
                    }
                }
            });
            // Move the card to the end of the player's hand if not already placed
            if (!card_dropped) {
                $('#your_hand').append($drag_card);

            }
            // Reset top and left properties to initial values
            $drag_card.css("top", "initial");
            $drag_card.css("left", "initial");;
            // Store the changed hand in the playingCards object
            playingCards.StoreMyHand();
        }
    });
}

// Add card_value attribute to card elements to allow value to be displayed in corner of card
playingCards.AddCardValueAttributes = function() {
    $('.card_value').each(function() {
        var card_value = $(this).text().trim();
        // add cardval attribute except to Jokers
        if (String($(this).text().trim()) !== String('?')) {
            $(this).attr("card_value", card_value);
        }
     });
}

// Update the player menu being viewed
playingCards.UpdatePlayerMenu = function(players, active_player, card_counts, wild_card) {
    // Update the wild card data being viewed on the player menu
    var $player_menu_ul = $('#player_menu>ul').clone();
    $player_menu_ul.find('#wild_card').text("Wild Card "+wild_card);
    // Get a copy of first players list element
    var $first_in_players_list = $('.players_list').first().clone();
    // Remove all the players from the player menu being viewed
    $player_menu_ul.find('.players_list').remove();
    // Generate the player elements and append to the new player menu
    var $new_players_list = null;
    for (var pndx=0; pndx<players.length; pndx++) {
        var $new_player = $first_in_players_list.clone(); // copy from original list
        $new_player.find('.player_card_count').text("+"+card_counts[pndx]);
        $new_player.find('.player_name').text(players[pndx]);
        if (String(players[pndx]) == String(active_player)) {
            $new_player.addClass('active');
            $new_player.find('.collapsible-header').addClass("teal");
            $new_player.find('.collapsible-header').addClass("lighten-2");
        } else {
            $new_player.removeClass('active');
            $new_player.find('.collapsible-header').removeClass("teal");
            $new_player.find('.collapsible-header').removeClass("lighten-2");
        }
        $new_player.appendTo($player_menu_ul);
    }
    // Replace the player menu being viewed with the newly generated menu
    $('#player_menu>ul').replaceWith($player_menu_ul);
}

// Update cards in player's hand being viewed
playingCards.UpdatePlayerCards = function(player_cards) {
    // Remove all the card elements being viewed in your_hand
    $('.players_card').remove();
    // Add card elements to your_hand to be viewed
    for (var ndx in player_cards) {
        // create new div element to store the card suit and value
        var $new_card = $("<div/>").appendTo("#your_hand");
        $new_card.addClass("players_card");
        $new_card.addClass("suit"+player_cards[ndx].suit);
        // create a new p element to store the card face value
        $new_card_faceval = $("<p/>").appendTo($new_card);
        $new_card_faceval.addClass("card_value");
        $new_card_faceval.text(player_cards[ndx].faceval);
    }
}

// Store my hand in playingCards object
playingCards.StoreMyHand = function() {
    var suit
    var faceval
    playingCards.my_hand = []
    $('#your_hand>.players_card').each(function() {
        faceval = $(this).text().trim();
        suit = playingCards.getSuit($(this));
        playingCards.my_hand.push({'suit':suit, 'faceval':faceval});
    });
}

// Store discards in playingCards object
playingCards.StoreDiscards = function() {
    var suit
    var faceval
    playingCards.discard_pile = []; // clear the discard pile
    $('.discard_pile_card').each(function() {
        faceval = $(this).text().trim();
        suit = playingCards.getSuit($(this));
        playingCards.discard_pile.push({'suit':suit, 'faceval':faceval});
    });
}

// Store game board in playingCards object
playingCards.StoreGameBoard = function() {

    // Clear the game board object
    playingCards.game_board = [];

    // Store each meld group by type and cards
    $('.game_board_meld_type').each(function() {
        var $meld_type_entry = $(this)
        var meld_cards = [];

        // Store each card for this meld in the game board object
        $meld_type_entry.siblings(".game_board_card").each(function() {
            var suit = playingCards.getSuit($(this));
            var faceval = $(this).first().text().trim();
            var player = $(this).attr("player");
            var user_name = $('#user_name').text();

            // Add my_played_card which will color the border of the card indicating ownership
            if (String(player) == String(user_name)) {
                $(this).addClass("my_played_card");
            }
            meld_cards.push({"player": player, "suit": suit, "faceval": faceval});
        });
        playingCards.game_board.push({"type": $meld_type_entry.text().trim(), "meld_cards": meld_cards});
    });
}

// Update game board with game board received from server
playingCards.UpdateGameBoard = function(game_board) {

    // Clear the gameboard view
    $('#game-board').children().remove();

    // Add each meld row to the game board view from the game board object
    for (var ndx in game_board) {
        // Add the type of meld entry
        var $meld_items_entry = $("<div/>").appendTo('#game-board');
        $meld_items_entry.addClass("game_board_meld_div");
        var $type_entry = $("<h4>").appendTo($meld_items_entry);
        $type_entry.addClass("game_board_meld_type");
        $type_entry.text(game_board[ndx].type);

        // Add each of the cards in the meld
        for (var mcdx in game_board[ndx].meld_cards) {
            var $meld_card_entry = $("<div>").appendTo($meld_items_entry);
            $meld_card_entry.addClass("suit"+game_board[ndx].meld_cards[mcdx].suit);
            $meld_card_entry.addClass("meld_card").addClass("game_board_card");
            $meld_card_entry.css("float", "left");
            $meld_card_entry.attr("player", game_board[ndx].meld_cards[mcdx].player);
            var $card_value_entry = $("<p>").appendTo($meld_card_entry);
            $card_value_entry.addClass("card_value");
            $card_value_entry.attr("card_value", game_board[ndx].meld_cards[mcdx].faceval);
            $card_value_entry.text(game_board[ndx].meld_cards[mcdx].faceval);
        }
    }
}

// Add card to player's hand being viewed
playingCards.AddPlayerCard = function(card) {
    // Append card to the player's current hand.
    var $add_card_div = $("<div/>").appendTo("#your_hand");
    $add_card_div.addClass("players_card");
    $add_card_div.addClass("suit"+card.suit);
    $add_card_div.css("float","left");
    var $card_value_p = $("<p/>").appendTo($add_card_div);
    $card_value_p.addClass("card_value");
    $card_value_p.text(card.faceval);
    playingCards.max_z_index++;
    $add_card_div.css("z-index", playingCards.max_z_index.toString());
    // Reset attributes for my hand
    playingCards.Initialize();
}

// highlight selection of card to discard when discard menu visible
playingCards.DiscardSelectOnClick = function(event) {
    var isVisible = $('#discard-selection-body').is(':visible');
    if (isVisible) { // collapse requested
        $('.players_card').off('click');
        $('.players_card').removeClass("discard");
    } else { // discard menu requested
        $('.players_card').on("click", function() {
            $players_card = $(this);
            // Remove discard class from all player cards
            $('.players_card').each(function() {
                $(this).removeClass('discard');
            });
            border_color = $players_card.css("border-color");
            // Add discard class to the selected card
            $players_card.addClass("discard");
         });
    }
}

// Discard selected - remove card from player's hand and move to discard pile
playingCards.DiscardCardFromHand = function() {
    // access the player's card element being discarded
    var $player_card = $('.players_card.discard');
    // extract the suit and faceval from the card being discarded
    var faceval = $player_card.text().trim();
    if (String(faceval) !== "") {
        var suit = playingCards.getSuit($player_card);
        // remove card from your_hand being viewed
        $player_card.remove();
        // add card to the discard pile being viewed
        playingCards.AddCardToDiscardPile(suit, faceval);
        // collapse the discard menu selector
        $('#discard-selection-body').hide();
        // Reset attributes for my hand
        playingCards.Initialize();
    } else {
        $('#status_msg').text("Select a card to discard!");
    }
}

// Add card to the discard pile being viewed
playingCards.AddCardToDiscardPile = function(suit, faceval) {
    // Append card to discard pile being viewed
    var $discard_div = $("<div/>").appendTo("#draw_discard_area");
    $discard_div.addClass("discard_pile_card");
    $discard_div.addClass("suit"+suit);
    $card_value_p = $("<p/>").appendTo($discard_div);
    $card_value_p.addClass("card_value");
    $card_value_p.text(faceval);
}

// Draw a card from the deck and add to the player's hand being viewed
playingCards.DrawCardFromDeck = function() {
    // retrieve the deck from the hidden field storage area
    var deck = $('#the_deck').text();
    // convert the deck to json format, extract the top card from the deck
    // convert the deck back to text format, and store in the hidden storage area
    var deck_json = JSON.parse(deck);
    var top_card = deck_json.pop(0);
    deck = JSON.stringify(deck_json);
    $('#the_deck').text(JSON.stringify(deck_json));
    // add the top card from the deck to the player's hand being viewed
    playingCards.my_hand.push(top_card);
    playingCards.AddPlayerCard(top_card);
    // update the number of cards in the user's hand being viewed
    playingCards.UpdateCardCount();
    // collapse the draw selection body
    $('#draw-selection-body').hide();
}

// Draw a card from the discard pile and add to the player's hand being viewed
playingCards.DrawCardFromDiscardPile = function() {

    if (playingCards.discard_pile.length != 0) {
        var top_card = playingCards.discard_pile.pop(0);
        // add the top card from the discard pile to the player's hand being viewed
        playingCards.my_hand.push(top_card);
        playingCards.AddPlayerCard(top_card);
        // update the number of cards in the user's hand being viewed
        playingCards.UpdateCardCount();
        // update the discard pile contents
        $('.discard_pile_card.suit'+top_card.suit).each(function() {
            var faceval=$(this).find('.card_value').text().trim();
            if (String(faceval) == String(top_card.faceval)) {
                $(this).remove();
            }
        });
        playingCards.StoreDiscards();
        // collapse the draw selection body
        $('#draw-selection-body').hide();
    } else {
        $('#status_msg').text("Draw from draw pile!  Discard pile is empty!");
    }
}

// update the card count on the players menu being viewed
playingCards.UpdateCardCount = function() {
    var user_name = $('#user_name').text();
    $('.player_name').each(function(){
        if (String($(this).text().trim()) == String(user_name)) {
            var num_cards = 0;
            for (var card in playingCards.my_hand) {
                num_cards++;
            }
            $(this).prev().text("+"+num_cards.toString());
         }
    });
}

// post the changes to the server and pass the torch to the next player
playingCards.TurnCompletePost = function() {
    // retrieve the deck from the hidden field storage area
    var deck = $('#the_deck').text();
    var my_hand = JSON.stringify(playingCards.my_hand);
    var discard_pile = JSON.stringify(playingCards.discard_pile);
    var game_board = [];

    if (playingCards.game_board) {
        game_board = JSON.stringify(playingCards.game_board);
    }

    // send the updated deck, players hand and discard pile back to the server
    $.ajax({
        url : "turn_complete_post/", // the endpoint
        type : "POST", // http method
        data : {
            updated_deck : deck,
            updated_players_hand : my_hand,
            discards : discard_pile,
            game_board: game_board,
            csrfmiddlewaretoken : $('input[name=csrfmiddlewaretoken]').val(),
        },
        // handle a successful response
        success : function(json) {
            //console.log(json); // log the returned json to the console
            //console.log("success"); // another sanity check

            // Reload the page to obtain server updates
            location.reload();
        },
        // handle a non-successful response
        error : function(xhr,errmsg,err) {
            console.log("ajax error");
        }
    });
    // collapse the turn complete menu
    $('#turn-complete-body').hide();
}

// Function to check for updates from the server via server sent events - SSE
playingCards.CheckForServerEvents = function () {
    var user_name = $('#user_name').text();
    var game_id = $('#game_id').text();
    if ((String(user_name) != String("")) && (String(game_id) != String("")))
    {
        if(typeof(EventSource) !== "undefined") {
            // create new SSE - server side event object
            var source = new EventSource("/stream/"+game_id+"/"+user_name);
            // check for messages from the server
            source.onmessage = function(event) {
                var json = JSON.parse(event.data);
                if (String(json.type) == String('update_game')) {
                    playingCards.UpdatePlayerCards(json.player_cards);
                    $('#the_deck').text(JSON.stringify(json.deck_cards));
                    // clear stored discard_pile object
                    playingCards.discard_pile = []
                    // remove all cards from the discard pile being viewed
                    $('.discard_pile_card').remove();
                    // add each card to the discard pile being viewed
                    for (var ndx in json.discards) {
                        playingCards.AddCardToDiscardPile(json.discards[ndx].suit, json.discards[ndx].faceval);
                    }
                    // update the player menu being viewed
                    playingCards.UpdatePlayerMenu(json.players, json.active_player, json.card_counts, json.wild_card);
                    // update the dealer name being viewed
                    $('#dealer').text("Dealer: "+json.dealer);
                    // Update game board with game board received from server
                    playingCards.UpdateGameBoard(json.gameboard);
                    // Re-initialize after receiving server updates
                    playingCards.Initialize();
                }
            };
        }
    }
}

// highlight selection of cards from your hand to play when play menu visible
playingCards.PlaySelectOnClick = function(play_type) {
    var play_id = "#play-"+play_type+"-selection-body";
    var isVisible = $(play_id).is(':visible');
    // remove meld_card class from all cards in your hand
    $('.players_card').off('click');
    $('.players_card').removeClass("meld_card");
    playingCards.meld_order = 0;
    // add click handlers to each card when the play selection menus are opened
    if (!isVisible) {
        // handle the click event on the cards in your hand
        $('.players_card').on("click", function() {
            border_color = $(this).css("border-color");
            // Add meld_card class to selected cards in your hand
            if (String(border_color) == String("rgb(0, 0, 0)")) {
                playingCards.meld_order++; // used to identify the order of selection
                $(this).addClass("meld_card");
                $(this).attr("meld_order", playingCards.meld_order.toString());
            // otherwise remove meld_card class from cards that are de-selected in your hand
            } else {
                $(this).removeClass("meld_card");
                $(this).removeAttr("meld_order");
            }
        });
    }
}

// highlight selection of melds from the game board when play add menu visible
playingCards.PlayGameBoardSelectOnClick = function() {
    var isVisible = $('#play-add-selection-body').is(':visible');
    // remove card-selected class from all cards on the game board
    $('.card-selected').each(function() {
        $(this).off();
        $(this).removeClass("card-selected");
    });
    // add click handlers to the game board melds when the add to game board selection menu is opened
    if (!isVisible) { // play add requested (selected while menu was collapsed)
        $('#game-board>div').each(function() {
            var $game_board_div = $(this);
            $game_board_div.off();
            // handle the click event on the game board meld areas
            $game_board_div.on("click", function(event) {
                var set_background_color = true;
                var $clicked_game_board_div = $(this);
                $clicked_game_board_div.find('.card_value').each(function() {
                    var background_color = $(this).css("background-color");
                    if (String(background_color) == String("rgb(255, 255, 0)")) {
                        set_background_color = false;
                    }
                });
                // clear out any previously selected melds by removing card-selected class
                $('#game-board').find(".card_value").each(function() {
                    $(this).parent().removeClass("card-selected");
                });
                // highlight the card meld that was selected by adding card-selected class
                if (set_background_color) {
                    $clicked_game_board_div.find(".card_value").each(function() {
                        $(this).parent().addClass("card-selected");
                    });
                }
            });
        });
    }
}

// move cards from the player's hand as a run or a book to the game board
// where a run is a sequence of cards --2,3,4--, --10,J,Q,K--
// and a book is a group of cards with the same face value --Q hearts, Q diamonds, Q clubs---
playingCards.PlayCardsNew = function(play_type) {
    var user_name = $('#user_name').text().trim();
    var cards_selected = 0;
    $('.players_card.meld_card').each(function() {
        cards_selected++;
    });
    // check to see cards selected to play
    if (cards_selected > 0) {
        // sort the cards by selection order to place on the game board
        var $ordered_meld_cards = $('.players_card.meld_card').sort(function(a, b) {
            var contentA = parseInt($(a).attr('meld_order'));
            var contentB = parseInt($(b).attr('meld_order'));
            return (contentA < contentB) ? -1 : (contentA > contentB) ? 1 : 0;
        });
        // create new game-board entry
        var $game_board_entry = $("<div/>").appendTo("#game-board");
        $game_board_entry.addClass("game_board_meld_div");
        var $meld_type_entry = $("<h4>"+play_type+"</h4>").appendTo($game_board_entry);
        $meld_type_entry.addClass("game_board_meld_type");
        // create new card in the new game-board entry
        var meld_cards_list=[];
        $ordered_meld_cards.each(function() {
            var $new_card = $(this).clone();
            $new_card.appendTo($game_board_entry);
            $new_card.addClass("my_played_card");
            $new_card.attr("player", user_name);
            // add to playingCards gameboard object
            var suit = playingCards.getSuit($new_card);
            meld_cards_list.push({"player": user_name,
                                  "suit": suit, "faceval": $new_card.text().trim()});
        });
        playingCards.game_board.push({"type": play_type, "meld_cards": meld_cards_list});

        // add spacing between card melds
        $break_entry = $("<br clear='all' />").appendTo("#game-board");
        // change the class from players_card to game_board_card for each game-board card
        $('#game-board').find('.players_card').each(function() {
            $(this).removeClass("players_card draggable").addClass("game_board_card");
            $(this).css("float", "left");
        });
        // remove the card from the player's hand
        $('.players_card.meld_card').remove();
        // Reset attributes for my hand
        playingCards.Initialize();
    } else {
        $('#status_msg').text("Select cards from your hand to play!");
    }
}

// move cards from the player's hand before or after a selected meld on the game board
playingCards.PlayCardsAdd = function(play_type) {
    var user_name = $('#user_name').text().trim();
    var cards_selected = false;
    var game_board_selected = false;
    if ($('.players_card').hasClass("meld_card")) {
        cards_selected = true;
    }
    $('#game-board').find(".card-selected").each(function() {
        game_board_selected = true;
     });

    // check to see cards selected to play and game board section selected to place the cards
    if (cards_selected && game_board_selected) {
        // sort the cards by selection order to place on the game board
        var $ordered_meld_cards = $('.players_card.meld_card').sort(function(a, b) {
            var contentA = parseInt($(a).attr('meld_order'));
            var contentB = parseInt($(b).attr('meld_order'));
            return (contentA < contentB) ? -1 : (contentA > contentB) ? 1 : 0;
        });
        // find the first and last card elements to allow insertion of selected cards to the game board
        var $first_card_selected = null
        var $last_card_selected = null
        $('#game-board').find(".card-selected").each(function() {
            if (!$first_card_selected) {
                $first_card_selected = $(this);
            }
            $last_card_selected = $(this);
        });
        // insert before/after the selected player's cards to the selected game board section
        if (play_type == String("Before")) {
            $ordered_meld_cards.insertBefore($first_card_selected);
        } else {
            $ordered_meld_cards.insertAfter($last_card_selected);
        }
        // remove the meld_card class from the inserted cards
        // and add the my_played_card class to the inserted cards
        $ordered_meld_cards.each(function() {
            $(this).removeClass('meld_card');
            $(this).addClass("my_played_card");
            $(this).attr("player", user_name);
        });
        // remove the card from the player's hand
        $('.players_card.meld_card').remove();
        // change the class from players_card to game_board_card for each game-board card
        $('#game-board').find('.players_card').each(function() {
            $(this).removeClass("players_card draggable").addClass("game_board_card");
            $(this).css("float", "left");
        });
        // remove highlighted color from selected cards
        $('.card-selected').find('.card_value').each(function() {
            $(this).parent().removeClass('card-selected');
        });
        // Store updated game board to game board object
        playingCards.StoreGameBoard();
        // Reset attributes for my hand
        playingCards.Initialize();
    } else {
        if (cards_selected) {
            $('#status_msg').text("Select game board section to play the cards!");
        } else {
            $('#status_msg').text("Select cards from your hand to play!");
        }
    }
}


// MAIN after document is loaded
$(document).ready(function() {
    // Add the SVG for the back of the card image
    $('.draw_pile_card').append(card_svg);
    // materials initialization
    $('.collapsible').collapsible();
    // perform iniitalization
    playingCards.Initialize();
    // check for server updates
    playingCards.CheckForServerEvents();
    // reset menu selections when deal menu selected
    $('#deal-selection-header').on('click', function(event) {
        playingCards.ResetMenuSelections();
    });
    // perform draw card action when selected
    $('#draw_pile_button').on('click', function(event) {
        playingCards.DrawCardFromDeck();
    });
    // perform draw card from discard pile action when selected
    $('#draw_discard_button').on('click', function(event) {
        playingCards.DrawCardFromDiscardPile();
    });
    // reset menu selections when draw menu selected
    $('#draw-selection-header').on('click', function(event) {
        playingCards.ResetMenuSelections();
    });
    // allow selection of discard upon clicking discard from menu
    $('#discard-selection-header').on('click', function(event) {
        playingCards.ResetMenuSelections();
        playingCards.DiscardSelectOnClick(event);
    });
    // perform discard action when selected
    $('#discard_button').on("click", function() {
        playingCards.DiscardCardFromHand();
    });
    // reset menu selections when undue menu selected
    $('#undue-header').on("click", function(event) {
        playingCards.ResetMenuSelections();
    });
    // perform undue action when seleected
    $('#undue_button').on("click", function(event) {
        // simply reload the page from the server and get game data prior to last complete turn update
        location.reload();
    });
    // reset menu selections when complete menu selected
    $('#turn-complete-header').on('click', function(event) {
        playingCards.ResetMenuSelections();
    });
    // complete the user's turn and pass updates to the server when selected
    $('#complete_button').on('click', function(event) {
        playingCards.TurnCompletePost();
    });
    // allow selection of cards from playing hand upon clicking play from menu
    $('#play-new-selection-header').on('click', function(event) {
        playingCards.ResetMenuSelections();
        playingCards.PlaySelectOnClick('new');
    });
    $('#play-add-selection-header').on('click', function(event) {
        playingCards.ResetMenuSelections();
        playingCards.PlaySelectOnClick('add');
        playingCards.PlayGameBoardSelectOnClick();
    });
    // play cards as a run on the game board
    $('#play_run_button').on('click', function(event) {
        playingCards.PlayCardsNew("Run");
    });
    // play cards as a book on the game board
    $('#play_book_button').on('click', function(event) {
        playingCards.PlayCardsNew("Book");
    });
    // play cards before a selected game board meld
    $('#play_add_before_button').on('click', function(event) {
        playingCards.PlayCardsAdd("Before");
    });
    // play cards after a selected game board meld
    $('#play_add_after_button').on('click', function(event) {
        playingCards.PlayCardsAdd("After");
    });
});
