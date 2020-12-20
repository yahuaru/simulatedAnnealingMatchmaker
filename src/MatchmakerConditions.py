from player import PlayerType

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

TEAMS_NUM = 3

TEAM_SIZE = 3


class Team:
    def __init__(self, division=[]) -> None:
        self.divisions = division
        self.playersTypesNum = {
            playerType: 0 for playerType in list(PlayerType)
        }
        self.maxLevel = 0
        for division in self.divisions:
            self.playersTypesNum[division.type] += 1
            self.maxLevel = max(self.maxLevel, division.level)
        self.size = len(self.divisions)

    def addPlayer(self, player):
        self.divisions.append(player)
        self.playersTypesNum[player.type] += 1
        self.size += 1

    def removePlayer(self, player):
        self.divisions.remove(player)
        self.playersTypesNum[player.type] -= 1
        self.size -= 1

    def copy(self):
        return Team(self.divisions.copy())

    def __repr__(self) -> str:
        res = "Team(divisions={}, playersTypeNum={}, maxLevel={}, size={})"
        return res.format(self.divisions, self.playersTypesNum, self.maxLevel,
                          self.size)


class BattleGroup:
    def __init__(self, teams=[]) -> None:
        self.teams = teams

    def size(self):
        return len(self.teams)

    def copy(self):
        teams = [team.copy() for team in self.teams]
        return BattleGroup(teams)

    def __repr__(self) -> str:
        teamsRepr = ""
        for team in self.teams:
            teamsRepr += "\t{}\n".format(team)
        return "BattleGroup[\n{}\n\t]".format(teamsRepr)
