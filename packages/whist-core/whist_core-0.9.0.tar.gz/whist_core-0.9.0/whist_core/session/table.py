"""DAO of session."""
from typing import Any, Union

from pydantic import model_validator
from typing_extensions import Literal

from whist_core.error.table_error import TableFullError, TeamFullError, TableNotReadyError, \
    TableNotStartedError, TableSettingsError
from whist_core.game.errors import RubberNotDoneError
from whist_core.game.rubber import Rubber
from whist_core.session.matcher import Matcher, subclass_registry
from whist_core.session.session import Session
from whist_core.user.player import Player


class Table(Session):
    """
    The game logics instance of a room to play Whist.
    """
    min_player: int
    max_player: int
    team_size: int = 2
    started: bool = False
    rubbers: list[Rubber] = []
    matcher: Matcher

    # copied from
    # https://blog.devgenius.io/deserialize-child-classes-with-pydantic-that-gonna-work-784230e1cf83
    def __init__(self, **data: Any) -> None:
        """
        Constructor
        :param data: fields from above
        """
        matcher = data['matcher']
        if isinstance(matcher, dict):
            item_matcher_keys = sorted(matcher.keys())
            for _, subclass in subclass_registry.items():
                matcher_keys = sorted(subclass.__fields__.keys())
                if item_matcher_keys == matcher_keys:
                    matcher = subclass(**matcher)
                    break
            data['matcher'] = matcher
        super().__init__(**data)

    def model_dump(self, *, mode: Union[Literal['json', 'python'], str] = 'python', include=None,
                   exclude=None, by_alias: bool = False, exclude_unset: bool = False,
                   exclude_defaults: bool = False, exclude_none: bool = False,
                   round_trip: bool = False, warnings: bool = True) -> dict[str, Any]:
        """
        Overrides model_dump to ensure matcher is correctly dumped.
        :param mode:
        :param include:
        :param exclude:
        :param by_alias:
        :param exclude_unset:
        :param exclude_defaults:
        :param exclude_none:
        :param round_trip:
        :param warnings:
        :return:
        """
        model = super().model_dump(mode=mode, include=include, exclude=exclude, by_alias=by_alias,
                                   exclude_unset=exclude_unset, exclude_defaults=exclude_defaults,
                                   exclude_none=exclude_none, round_trip=round_trip,
                                   warnings=warnings)
        model['matcher'] = self.matcher.model_dump()
        return model

    # pylint: disable=no-self-argument
    @model_validator(mode="before")
    @classmethod
    def validate_min_is_lower_max_player(cls, values):
        """
        Checks if the min_player is less or equal than max_player.
        :param values:
        :return:
        """
        if values.get('min_player') > values.get('max_player'):
            raise TableSettingsError('The amount of minimum player must not be higher than the '
                                     'maximum amount.')
        return values

    def __len__(self):
        """
        The amount of players joined.
        :return: # player
        :rtype: int
        """
        return len(self.users)

    @property
    def ready(self) -> bool:
        """
        Flag if the table is ready to start playing.
        :return Ready or not
        :rtype: boolean
        """
        return len(self.users) >= self.min_player and self.users.ready

    @property
    def current_rubber(self) -> Rubber:
        """
        Returns the current rubber
        :return: the latest rubber entry
        """
        if not self.started:
            raise TableNotStartedError()
        return self.rubbers[-1]

    def next_rubber(self) -> Rubber:
        """
        Creates the next rubber. In order to create the first rubber use 'Table.start()'.
        :return: the new rubber
        """
        if len(self.rubbers) == 0:
            raise TableNotStartedError()
        if self.rubbers[-1].done:
            self.rubbers.append(self._create_rubber())
        else:
            raise RubberNotDoneError()
        return self.current_rubber

    def start(self) -> None:
        """
        Starts the table, but will check if every player is ready first.
        """
        if not self.ready:
            raise TableNotReadyError()

        self.rubbers.append(self._create_rubber())
        self.started = True

    def join(self, player: Player) -> None:
        """
        If a seat is available a player joins the table.
        :param player: who wants to join the table
        :type player: Player
        :return: None or raised an error if the table is already full.
        :rtype: None
        """
        if len(self.users) < self.max_player:
            self.users.append(player)
        else:
            raise TableFullError(f'Table with name: {self.name} is already full.')

    def leave(self, player: Player) -> None:
        """
        Remove a player from table.
        :param player: The player to remove.
        :type player: Player
        :return: None
        :rtype: None
        """
        self.users.remove(player)

    def join_team(self, player: Player, team: int) -> None:
        """
        Player joins a team.
        :param player: to join a team
        :type player: Player
        :param team: id of the new team
        :type team: int
        :return: None if successful or raises Error if team is full
        :rtype: None
        """
        if not self.users.is_joined(player):
            self.join(player)
        team_size = self.users.team_size(team)
        if team_size >= self.team_size:
            raise TeamFullError(f'Team with id: {team} is already full.')
        self.users.change_team(player, team)

    def player_ready(self, player) -> None:
        """
        Player says they is ready.
        :param player: player who is ready
        :type player: Player
        :return: None
        :rtype: None
        """
        self.users.player_ready(player)

    def player_unready(self, player) -> None:
        """
        Player says they is not ready.
        :param player: player who is not ready
        :type player: Player
        :return: None
        :rtype: None
        """
        self.users.player_unready(player)

    def _create_rubber(self):
        distribution = self.matcher.distribute(users=self.users)
        self.users.apply_distribution(distribution)
        teams = self.users.teams
        rubber = Rubber(teams=teams)
        return rubber
