"""Errors in game phase"""
from whist_core.user.player import Player


class CardNotInHandError(Exception):
    """
    Raised when a player tries to play a card, that is not in their hand.
    """


class HandDoneError(Exception):
    """
    Raised when the next trick is requested, but current Hand is already done..
    """


class HandNotDoneError(Exception):
    """
    Raised when the next hand is requested, but current is not done yet.
    """


class GameNotDoneError(Exception):
    """Raised if next game is requested, but current is not done yet."""


class GameNotStartedError(Exception):
    """
    Raised if a game has not be started.
    """


class NotPlayersTurnError(Exception):
    """
    Raised when players tries to play although is not their turn.
    """

    def __init__(self, player: Player, turn_player: Player):
        """
        Constructor.
        :param player: Who tried to play a card.
        :param turn_player: Which turn it actually is.
        """
        super().__init__()
        self.message = f'Is not {player} turn, but {turn_player}.'


class NoTrumpSelectedError(Exception):
    """
    Raised when no trump is selected for hand.
    """


class RubberNotDoneError(Exception):
    """
    Raised if the current rubber is not done, but action requested requires it to be done.
    """


class TrickDoneError(Exception):
    """
    Raised when the trick is already done.
    """
