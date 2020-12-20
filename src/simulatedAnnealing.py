import random
from typing import Tuple
from player import PlayerType
from MatchmakerConditions import BattleGroup, SHIP_TYPE_DIFFERENCE, TEAMS_NUM, TEAM_SIZE
import math

INITIAL_TEMP = 1
TEMP_DECREASE_COEFFICIENT = 0.9


class SimulatedAnnealingMatchmaker:
    def __init__(self):
        self.GENERATE_ACTIONS = [self.swapTeamMembers, self.addPlayer, self.removePlayer]

        self.queue = []
        self.__initProcess()

    def __initProcess(self):
        self.__currentBattleGroup = BattleGroup(size=TEAMS_NUM)
        self.__prev_energy = self.__getEnergy(self.__currentBattleGroup)
        self.current_temperature = INITIAL_TEMP

    def enqueueDivision(self, division):
        self.queue.append(division)

    def dequeueDivision(self, division):
        self.queue.remove(division)

    def proccessBattleGroups(self) -> Tuple:
        current_candidate = self.__generateCandidate(self.__currentBattleGroup)
        current_energy = self.__getEnergy(self.__currentBattleGroup)
        if current_energy == 0:
            resultBattleGroup = self.__currentBattleGroup
            self.__initProcess()
            return True, resultBattleGroup

        if current_energy < self.__prev_energy:
            prob = math.exp(-(current_energy - self.__prev_energy) / self.current_temperature)
            if random.random() < prob:
                self.__currentBattleGroup = current_candidate
        else:
            self.__currentBattleGroup = current_candidate

        self.current_temperature *= TEMP_DECREASE_COEFFICIENT
        return False, None

    def __generateCandidate(self, battleGroup) -> BattleGroup:
        newBattleGroup = battleGroup.copy()
        actions = list(self.GENERATE_ACTIONS)
        successful = False
        while not successful and actions:
            action = actions.pop(random.randint(0, len(actions) - 1))
            successful = action(newBattleGroup)

        return newBattleGroup

    def swapTeamMembers(self, battleGroup) -> bool:
        teams = list(battleGroup.teams)
        team1 = random.choice(teams)
        teams.remove(team1)
        team2 = random.choice(teams)

        if team1.size == 0 or team2.size == 0:
            return False
        
        playerTeam1 = random.choice(team1.divisions)
        team1.removePlayer(playerTeam1)
        
        playerTeam2 = random.choice(team2.divisions)
        team2.removePlayer(playerTeam2)
        
        team1.addPlayer(playerTeam2)
        team2.addPlayer(playerTeam1)
        
        return True

    def addPlayer(self, battleGroup):
        if not self.queue:
            return False
        vacantTeams = [team for team in battleGroup.teams if team.size < TEAM_SIZE]
        if not vacantTeams:
            return False
        vacantTeam = random.choice(vacantTeams)
        vacantTeam.addPlayer(self.queue.pop(0))
        return True

    def removePlayer(self, battleGroup):
        teamsWithPlayers = [team for team in battleGroup.teams if team.size > 0]
        if not teamsWithPlayers:
            return False
        teamWithPlayers = random.choice(teamsWithPlayers)
        player = random.choice(teamWithPlayers.divisions)
        teamWithPlayers.removePlayer(player)
        self.queue.append(player)

    @staticmethod
    def __getEnergy(battleGroup):
        energy = 0
        for i, team in enumerate(battleGroup.teams):
            for otherTeam in battleGroup.teams[i:]:
                for playerType in list(PlayerType):
                    if abs(otherTeam.playersTypesNum[playerType] - team.playersTypesNum[playerType]) > SHIP_TYPE_DIFFERENCE[playerType]:
                        energy += 1
            if team.size < TEAM_SIZE:
                energy += 1
        return energy