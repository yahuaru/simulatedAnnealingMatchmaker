from player import PlayerType

INITIAL_TEMPERATURE = 6

SHIP_TYPE_DIFFERENCE = {
    PlayerType.ALPHA: 0,
    PlayerType.BETA: 0,
    PlayerType.GAMMA: 0,
}

SHIP_TYPE_NUM = {
    PlayerType.ALPHA: 0,
    PlayerType.BETA: 0,
    PlayerType.GAMMA: 0,
}

MAX_LEVEL_DIFFERENCE = 1

MAX_PING_DIFFERENCE = 10

TEAMS_NUM = 4

TEAM_SIZE = 3


class Division:
    def __init__(self):
        self.players = []
        self.size = 0
        self.playersTypesNum = {playerType: 0 for playerType in list(PlayerType)}
        self.maxLevel = 0

    def addPlayer(self, player):
        self.size += 1
        self.players.append(player)
        self.playersTypesNum[player.type] += 1
        self.maxLevel = max(self.maxLevel, player.level)

    def __repr__(self):
        res = "Division(players={}, playersTypeNum={}, maxLevel={}, size={})"
        return res.format(self.players, self.playersTypesNum, self.maxLevel, self.size)


class Team:
    def __init__(self, division=None) -> None:
        self.divisions = division if division is not None else []
        self.playersTypesNum = {playerType: 0 for playerType in list(PlayerType)}
        self.maxLevel = 0
        for division in self.divisions:
            for playerType in list(PlayerType):
                self.playersTypesNum[playerType] += division.playersTypesNum[playerType]
            self.maxLevel = max(self.maxLevel, division.maxLevel)
        self.size = len(self.divisions)

    def addDivision(self, division):
        self.divisions.append(division)
        for playerType in list(PlayerType):
            self.playersTypesNum[playerType] += division.playersTypesNum[playerType]
        self.size += division.size

    def removeDivision(self, division):
        self.divisions.remove(division)
        for playerType in list(PlayerType):
            self.playersTypesNum[playerType] -= division.playersTypesNum[playerType]
        self.size -= division.size

    def copy(self):
        return Team(self.divisions.copy())

    def __repr__(self) -> str:
        res = "Team(divisions={}, playersTypeNum={}, maxLevel={}, size={})"
        return res.format(self.divisions, self.playersTypesNum, self.maxLevel, self.size)


class BattleGroup:
    def __init__(self, teams=None) -> None:
        self.teams = teams if teams is not None else []

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
