"""
Name
    forms.py

DESCRIPTION
    Provides form data to be entered by the user to create or join a Blitz game

CLASS
    GameSettingsForm               -- object to define the user selections for creating a new Blitz game
    GameJoinForm                   -- defines the user selections for joining an already created game

FUNCTION
    clean                          -- returns the cleaned form data; when joining a game validation is
                                      also performed to ensure the game exists and that it is a new user
                                      name selected

DATA
    forms                          -- contains the forms data entered by the user
    games                          -- contains any active game data (players, cards, ...)
"""

from django import forms
from django.core.validators import RegexValidator

alphanumeric = RegexValidator(r'^[0-9a-zA-Z]*$', 'Only alphanumeric characters are allowed.')

DECK_COUNT=[
    (1, "One"),
    (2, "Two"),
]


# GameSettingsForm class defines the user selections for creating a new Blitz game
class GameSettingsForm(forms.Form):
    user_name = forms.CharField(label='User Name', max_length=100,
                                error_messages={'required': "Enter your name - only alphanumeric characters"},
                                validators=[alphanumeric])
    game_id = forms.CharField(label='Game ID', max_length=100,
                              error_messages={'required': "Enter your name - only alphanumeric characters"},
                              validators=[alphanumeric])
    number_of_jokers = forms.IntegerField(min_value=0, max_value=6, required=False)
    number_of_decks = forms.ChoiceField(widget=forms.RadioSelect, choices=DECK_COUNT, initial=('One', 1))

    def clean(self):
        game_id = self.cleaned_data['game_id']
        if self.games.get_game(game_id):
            self._errors['game_id'] = self.error_class([
                'Game with ID:' + game_id + ' -- Already In Use'])
        return self.cleaned_data


# GameJoinForm class defines the user selections for joining an already created game
class GameJoinForm(forms.Form):

    user_name = forms.CharField(label='User Name', max_length=100,
                                error_messages={'required': "Enter your name - only alphanumeric characters"},
                                validators=[alphanumeric])
    game_id = forms.CharField(label='Game ID', max_length=100,
                              error_messages={'required': "Enter your name - only alphanumeric characters"},
                              validators=[alphanumeric])

    # the clean performs validation that the game_id selected exists, and
    # that the user name has not already been used
    def clean(self):
        user_name = self.cleaned_data['user_name']
        game_id = self.cleaned_data['game_id']
        if self.games.get_game(game_id):
            if user_name in self.games.get_players(game_id):
                self._errors['user_name'] = self.error_class([
                    'User Name Already In Use'])
        else:
            self._errors['game_id'] = self.error_class([
                'GameId-'+game_id+' Not Found'])

        return self.cleaned_data

