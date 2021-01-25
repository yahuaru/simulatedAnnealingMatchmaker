from collections import namedtuple
from enum import IntEnum, auto


class PlayerType(IntEnum):
    ALPHA = auto()
    BETA = auto()
    GAMMA = auto()


Player = namedtuple("Player", ["type", "level"])
