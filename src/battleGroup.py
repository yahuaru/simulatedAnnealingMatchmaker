from player import PlayerType


class Division:
    def __init__(self, division_id, players=None, enqueue_time=0.0):
        self.id = division_id
        self.players = players if players is not None else []
        self.size = len(self.players)
        self.players_types_num = {playerType: 0 for playerType in list(PlayerType)}
        self.maxLevel = 0
        for player in self.players:
            self.players_types_num[player.type] += 1
            self.maxLevel = max(self.maxLevel, player.level)
        self.enqueue_time = enqueue_time

    def addPlayer(self, player):
        self.size += 1
        self.players.append(player)
        self.players_types_num[player.type] += 1
        self.maxLevel = max(self.maxLevel, player.level)

    def __repr__(self):
        res = "Division(players={}, playersTypeNum={}, maxLevel={}, size={})"
        return res.format(self.players, self.players_types_num, self.maxLevel, self.size)


class Team:
    def __init__(self, division=None) -> None:
        self.divisions = division if division is not None else []
        self.players_types_num = {playerType: 0 for playerType in list(PlayerType)}
        self.size = 0
        self.min_enqueue_time = min(division.enqueue_time for division in self.divisions) if self.divisions else 0
        for division in self.divisions:
            for playerType in list(PlayerType):
                self.players_types_num[playerType] += division.players_types_num[playerType]
            self.size += division.size

    def addDivision(self, division):
        self.divisions.append(division)
        for playerType in list(PlayerType):
            self.players_types_num[playerType] += division.players_types_num[playerType]
        self.size += division.size
        if self.divisions:
            self.min_enqueue_time = min(self.min_enqueue_time, division.enqueue_time)
        else:
            self.min_enqueue_time = division.enqueue_time

    def removeDivision(self, division):
        self.divisions.remove(division)
        for playerType in list(PlayerType):
            self.players_types_num[playerType] -= division.players_types_num[playerType]
        self.size -= division.size
        self.min_enqueue_time = min(d.enqueue_time for d in self.divisions) if self.divisions else 0

    def copy(self):
        return Team(self.divisions.copy())

    def __repr__(self) -> str:
        res = "Team(divisions:{}, playersTypeNum:{}, size:{}, min_enqueue_time:{})"
        return res.format(self.divisions, self.players_types_num, self.size, self.min_enqueue_time)


class BattleGroup:
    def __init__(self, teams=None) -> None:
        self.teams = teams if teams is not None else []
        self.min_enqueue_time = min(team.min_enqueue_time for team in self.teams) if self.teams else 0

    def size(self):
        return len(self.teams)

    def copy(self):
        teams = [team.copy() for team in self.teams]
        return BattleGroup(teams)

    def __repr__(self) -> str:
        teams_repr = ""
        for team in self.teams:
            teams_repr += "\t{}\n".format(team)
        return "BattleGroup[\n{}\n\t]".format(teams_repr)
