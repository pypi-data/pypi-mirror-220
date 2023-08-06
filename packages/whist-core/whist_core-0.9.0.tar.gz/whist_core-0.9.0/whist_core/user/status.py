"""
Data wrapper of player stati.
"""
from typing import Optional

# Wrapper class
# pylint: disable=too-few-public-methods
from pydantic import BaseModel


class Status(BaseModel):
    """
    Player status a table.
    """
    ready: bool = False
    team: Optional[int] = None
