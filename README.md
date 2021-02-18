# playcards - A Blitz Card Game
Blitz is a Rummy style card game.  The first card dealt to a player determines
the number of cards they are dealt (numbered cards indicate the number to deal where
face cards, aces, and jokers result in 10 cards being dealt).  The dealer's first card
also determines an additional wild card value for the hand.<br><br>
On a player's turn they can draw one card from the draw pile or multiple cards from the
discard pile, however, they must be able to play the last card they pick up from the 
discard pile.  After drawing cards a player may play cards to the game board by selecting
cards of the same face value and playing them as 'Books', or selecting cards of the same
suit in order (2, 3, 4,...) and playing them as 'Runs'.  Jokers and Wild Cards can take
on any value or suit.  Aces can be played before a 2 or after a King (high or low).  At
the end of their turn they must then discard a card from the hand.  If a player plays
all their cards to the game board and does not discard or have remaining cards in their
hand - they have Blitzed.  The hand is over and everyone scores their hand.  If the player
discards and no longer has any cards, then the remaining players all get one more turn.<br>
## Starting a Game
1. A player can create a new game by selecting a user name, a unique game id, (optional)
number of jokers, choice of 1 or 2 decks.  After successfully creating a game a player enters
game mode.
2. A player can join an existing game by selecting a unique user name, and existing game id.
After successfully joing a game a player enters game mode.
## Game Mode
During game mode the player box indicates all the players in the game, the number of cards
in each player's hand, the current wild card, and the current active player.  Options for the 
active player include:
1. Deal-allows the player selecting 'Deal' to become the dealer and deal cards to all players.
The first card in the dealer's hand will be the wild card for the hand.  The next player in
the player list will be the active player.  And the dealer will be the last player to play
in the current hand.
3. Draw - allows a player to select to draw a card from the face down card deck or a card
from the discard pile.  A player can draw as many cards from the discard pile as long as they
play the last card drawn during their turn.
5. Play-New - this action allows a player to play a new 'Run' (cards with the same face
value) or a new 'Book' (consecutive cards of the same suit - 2,3,4 or 10,J.Q).  A player
must play atleast 3 cards to make a play to the game board.  The game board will highlight
the cards that were played by the player for future scoring.  Each player's game board
will show all played cards but only the cards they play will be highlighted.
7. Play-Add - this action allows a player to play cards on already played cards on the game
board.  A player can add cards to a 'Book' if they have a matching face value card.  And
they can play on a 'Run' if they have the card preceding the cards played or following the
cards played of the same suit.
9. Discard - when a player can no longer play cards on the game board they then select a
card to discard to the discard pile.
11. Undue - this action will allow the player to start their turn over.  Their hand and the
game board will return to the state it was at the beginning of the turn.  Other player's 
game boards do not display any changes until a player's turn is complete by selecting the
'Complete' action.
13. Complete - this action completes a player's turn, updates all players game boards, and
sets the active player to the next player.
## Scoring
The scoring occurs at the completion of each hand.  This application does not currently
perform the scoring.  The scoring is kept by a designated score keeper as follows:
1. Jokers - 500 points
2. Aces - 100 points
3. Wild Cards - 100 points
4. Face Cards (J, Q, K) and Numbered cards: 10 (only) - 10 points
5. Numbered cards: 2 thru 9 - 5 points
A player adds up all the points using the above scoring for all the cards they have
played to the game board (highlighted cards) and subtract the points using the above
scoring for any cards remaining in their hand
## Winning the Game
At the start of the game the players decide on a score to reach (ie. 1000 points).  The
player with the highest score at the of the hand when at least one player reaches the
designated score wins.
