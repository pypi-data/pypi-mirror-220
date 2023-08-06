"""Hand of whist"""
from typing import Optional, Any, Dict

import deprecation
from pydantic import BaseModel

from whist_core.cards.card import Card, Suit
from whist_core.cards.card_container import UnorderedCardContainer, OrderedCardContainer
from whist_core.game.errors import HandDoneError
from whist_core.game.play_order import PlayOrder
from whist_core.game.player_at_table import PlayerAtTable
from whist_core.game.trick import Trick
from whist_core.game.warnings import TrickNotDoneWarning
from whist_core.util import enforce_str_on_dict


class Hand(BaseModel):
    """
    Hand of whist.
    """
    tricks: list[Trick] = []
    trump: Suit

    def done(self) -> bool:
        """
        Check if the hand is done.
        :return: True if the hand is done, else False
        :rtype: bool
        """
        return len(self.tricks) == 13 and self.tricks[-1]

    @property
    def current_trick(self):
        """
        Returns the current trick.
        """
        return self.tricks[-1]

    @staticmethod
    def deal(play_order: PlayOrder) -> 'Hand':
        """
        Deals the hand and starts the first trick.
        :return: the first trick
        :rtype: Trick
        """
        deck = UnorderedCardContainer.full()
        card: Optional[Card] = None
        while deck:
            player = play_order.get_next_player()
            card = deck.pop_random()
            player.hand.add(card)
        trump = card.suit

        first_trick = Trick(play_order=list(play_order), stack=OrderedCardContainer.empty(),
                            trump=trump)
        hand = Hand(tricks=[first_trick], trump=trump)
        return hand

    def next_trick(self, play_order: PlayOrder) -> Trick:
        """
        Starts the next trick.
        :return: the next trick
        :rtype: Trick
        """
        if self.done():
            raise HandDoneError()
        if len(self.tricks) == 0:
            next_trick_order = play_order
        elif self.tricks[-1].done:
            next_trick_order = self._winner_plays_first_card(play_order)
        else:
            raise TrickNotDoneWarning()
        next_trick = Trick(play_order=list(next_trick_order), trump=self.trump)
        self.tricks.append(next_trick)
        return next_trick

    @deprecation.deprecated("Use 'model_dump()' instead")
    def dict(self, *args, **kwargs):
        """Returns as dictionary."""
        super_dict = super().dict(*args, **kwargs)
        return enforce_str_on_dict(super_dict, ['trump'])

    def model_dump(self, *, mode: str = 'python', include=None,
                   exclude=None, by_alias: bool = False, exclude_unset: bool = False,
                   exclude_defaults: bool = False, exclude_none: bool = False,
                   round_trip: bool = False, warnings: bool = True) -> Dict[str, Any]:
        """Returns as dictionary."""
        model = super().model_dump(mode=mode, include=include, exclude=exclude, by_alias=by_alias,
                                   exclude_unset=exclude_unset, exclude_defaults=exclude_defaults,
                                   exclude_none=exclude_none, round_trip=round_trip,
                                   warnings=warnings)
        return enforce_str_on_dict(model, ['trump'])

    def _winner_plays_first_card(self, play_order: PlayOrder) -> PlayOrder:
        winner: PlayerAtTable = self.tricks[-1].winner
        return play_order.rotate(winner)
