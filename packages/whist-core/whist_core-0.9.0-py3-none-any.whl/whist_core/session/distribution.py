"""Wraps player's team assignment."""
from pydantic import BaseModel


class DistributionEntry(BaseModel):
    """
    Player to team assignment.
    """
    player_index: int
    team_id: int


class Distribution(BaseModel):
    """
    All player to team assignment.
    """
    entries: list[DistributionEntry] = []

    def __iter__(self):
        """
        Iterates over all entries.
        """
        return iter(self.entries)

    def __len__(self):
        """
        Returns the list of entries.
        """
        return len(self.entries)

    def __getitem__(self, item: int) -> DistributionEntry:
        """
        Gets on specific entry.
        :param item: index of the item
        """
        return self.entries[item]

    def add(self, entry: DistributionEntry) -> None:
        """
        Adds a new entry to the list.
        :param entry: to be added
        :return: None
        """
        self.entries.append(entry)
