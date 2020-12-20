import random
from player import Player, PlayerType

min_level = 0
max_level = 10

min_ping = 1
max_ping = 10000

def generatePlayer():
    player_type = random.choice(list(PlayerType))
    level = random.randrange(min_level, max_level)
    ping = random.randrange(min_ping, max_ping)
    player = Player(player_type, level, ping)
    return player
