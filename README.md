# playcards - A Blitz Card Game
Blitz is a Rummy style card game.  The first card dealt to a player
determines the number of cards they are dealt (numbered cards indicate the number to deal;
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
1. Deal
2. Draw
3. Play-New
4. Play-Add
5. Discard
6. Undue
7. Complete
