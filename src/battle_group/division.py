from player import PlayerType


class Division:
    def __init__(self, division_id, players=None, enqueue_time=0.0):
        self.id = division_id
        self.players = players if players is not None else []
        self.size = len(self.players)
        self.players_types_num = {playerType: 0 for playerType in list(PlayerType)}
        self.max_level = 0
        for player in self.players:
            self.players_types_num[player.type] += 1
            self.max_level = max(self.max_level, player.level)
        self.enqueue_time = enqueue_time

    def add_player(self, player):
        self.size += 1
        self.players.append(player)
        self.players_types_num[player.type] += 1
        self.max_level = max(self.max_level, player.level)

    def __repr__(self):
        res = "Division(players={}, playersTypeNum={}, maxLevel={}, size={})"
        return res.format(self.players, self.players_types_num, self.max_level, self.size)