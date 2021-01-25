import random

from battleGroup import Division
from player import Player, PlayerType


def generateDivision(index, max_division_size, enqueue_time=0.0, min_level=0, max_level=0):
    division = Division(index, enqueue_time=enqueue_time)
    for i in range(random.randint(1, max_division_size)):
        player = Player(random.choice(list(PlayerType)), random.randint(min_level, max_level))
        division.addPlayer(player)
    return division
