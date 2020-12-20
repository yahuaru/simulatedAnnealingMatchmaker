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
    def __init__(self, division=None) -> None:
        self.divisions = division if division is not None else []
        self.playersTypesNum = {playerType: 0 for playerType in list(PlayerType)}
        for division in self.divisions:
            self.playersTypesNum[division.type] += 1
        self.maxLevel = max([division.level for division in self.divisions]) if self.divisions else 0
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

    # def addDivision(self, division):
    #     self.divisions.append(division)
    #     self.maxLevel = max()
    #     for player in division:
    #         self.playersTypesNum[player.type] += 1


class BattleGroup:
    def __init__(self, size=0, teams=None) -> None:
        self.teams = teams if teams is not None else [Team() for _ in range(size)]

    def copy(self):
        teams = [team.copy() for team in self.teams]
        return BattleGroup(teams=teams)