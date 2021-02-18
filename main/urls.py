"""
NAME
    urls.py

DESCRIPTION
    Provides a list of valid URLs accepted by the application.

ACCEPTABLEURLs:
    /                                                -- the home page to play Blitz game
    /create/                                         -- dialog with the user to create a new game
    /join/                                           -- dialog with the user to join an existing game
    /stream/<game_id>/<user>                         -- request to connect to the server from java script to
                                                        support game board updates
    /show-cards/<game_id>/                           -- show selected contents of the specified game, used
                                                        during testing
    /deal/<game_id>/<user>/                          -- shuffle the card deck and deal cards to each player
                                                        in specified game
    /exit/<game_id>/<user>/                          -- exit the selected game for the selected user
    /game-page/<game_id>/<user>/                     -- display the game board view for the selected user in
                                                        the specified game
    /game-page/<game_id>/<user>/turn_complete_post/  -- updates the game board on the server and sends the
                                                        updates to each player in the specified game
"""
from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.homepage, name="homepage"),
    path('create', views.create, name="create"),
    path('create/', views.create, name="create"),
    path('join/', views.join, name="join"),
    path('stream/<game_id>/<user_name>', views.stream, name="stream"),
    path('show-cards/<game_id>', views.show_cards, name="show-cards"),
    path('deal/<game_id>/<user_name>', views.deal, name="deal"),
    path('exit/<game_id>/<user_name>', views.exit, name="exit"),
    path('game-page/<game_id>/<user_name>/', views.gamepage, name="game-page"),
    path('game-page/<game_id>/<user_name>/turn_complete_post/', views.turncompletepost, name="turn-complete-post"),
]