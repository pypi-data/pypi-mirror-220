"""Player instance during the game phase."""
from pydantic import BaseModel

from whist_core.cards.card_container import UnorderedCardContainer
from whist_core.user.player import Player


class PlayerAtTable(BaseModel):
    """
    Wraps the current hand and player instance.
    """
    player: Player
    hand: UnorderedCardContainer
    team: int

    def __eq__(self, other):
        """Checks if the other is equal."""
        if not isinstance(other, PlayerAtTable):
            return False
        return self.player == other.player

    def __repr__(self):
        """String representation"""
        return f'PlayerAtTable: {self.player}'
