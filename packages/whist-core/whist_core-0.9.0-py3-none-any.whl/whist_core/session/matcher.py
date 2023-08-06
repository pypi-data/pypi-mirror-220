"""
Match making tool.
"""
import abc
import random
from itertools import permutations
from typing import Any

from pydantic import BaseModel

from whist_core.session.distribution import Distribution, DistributionEntry
from whist_core.session.userlist import UserList

subclass_registry = {}


# pylint: disable=too-few-public-methods
class Matcher(abc.ABC, BaseModel, extra='allow'):
    """
    Abstrakt class for player to teams matching.
    """
    teams: list[Distribution] = []
    number_teams: int

    def __init_subclass__(cls, **kwargs: Any) -> None:
        """
        Initializes the subclass
        :param kwargs: field from above
        :return: None
        """
        super().__init_subclass__(**kwargs)
        subclass_registry[cls.__name__] = cls

    @abc.abstractmethod
    def distribute(self, users: UserList) -> Distribution:
        """
        Distributes cards according to subclass implementation.
        :param users: the players to be distributed to teams
        :return: the list of teams with players distributed to them
        """
        raise NotImplementedError

    def _apply_distribution(self, distribution):
        self.teams.append(distribution)


class RoundRobinMatcher(Matcher):
    """
    Distributes the players in the order of the user list.
    """
    iteration: int = 0
    distributions: list[Distribution] = []

    def __init__(self, number_teams: int, **data):
        """
        Constructor. See details in base class.
        :param number_teams:
        :param team_size:
        :param data:
        """
        super().__init__(number_teams=number_teams, **data)

    def distribute(self, users: UserList) -> Distribution:
        """
        Distributes one player to each team each round in order of the user list. Repeats until
        the user list is empty.
        :param users: the players to be distributed to teams
        :return: the teams in round robin distribution
        """
        if len(self.distributions) != len(users):
            self.distributions = []
            self._precalculate_distributions(len(users))
        distribution = self.distributions[self.iteration]
        self.iteration += 1
        self._apply_distribution(distribution)

        return distribution

    def _precalculate_distributions(self, number_players: int):
        for distribution_int in sorted(
                set(permutations((x % self.number_teams for x in range(number_players))))):
            distribution = Distribution()
            for player_index, team_id in enumerate(distribution_int):
                distribution.add(DistributionEntry(player_index=player_index, team_id=team_id))
            self.distributions.append(distribution)


class RandomMatcher(Matcher):
    """
    Distributes the players randomly to teams.
    """

    def distribute(self, users: UserList) -> Distribution:
        """
        For given parameter distributes the players to teams.
        :return: None
        :rtype: None
        """
        players = users.players
        team_size: int = int(len(players) / self.number_teams)
        teams: list = list(range(0, team_size)) * self.number_teams
        distribution: Distribution = Distribution()
        for player_index in range(len(players)):
            team_id = random.choice(teams)  # nosec random
            teams.remove(team_id)
            distribution.add(DistributionEntry(player_index=player_index, team_id=team_id))

        self._apply_distribution(distribution)

        return distribution
