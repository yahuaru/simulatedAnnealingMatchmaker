import math
import random
from typing import Tuple

from MatchmakerConditions import (SHIP_TYPE_DIFFERENCE, TEAM_SIZE, TEAMS_NUM,
                                  BattleGroup, Team, MAX_LEVEL_DIFFERENCE)
from player import PlayerType

INITIAL_TEMP = 8
TEMP_DECREASE_COEFFICIENT = 0.9

MAX_ITERATIONS = 1000


class SimulatedAnnealingMatchmakerLogger:
    def __init__(self):
        self.iterations = []
        self.prob = []

    def logIteration(self, iteration, temperature, energy):
        self.iterations.append((iteration, temperature, energy))

    def logProb(self, iteration, prob):
        self.prob.append((iteration, prob))

    def logPlayer(self, player):
        pass


class SimulatedAnnealingMatchmaker:
    def __init__(self, logger=None):
        self.GENERATE_ACTIONS = [self.swapTeamMembers, self.addPlayer, self.removePlayer]

        self.logger = logger

        self.queue = []
        self.__current_battle_group = None
        self.__current_temperature = INITIAL_TEMP
        self.__prev_energy = 0
        self.__current_iteration = 0
        self.initProcess()

    def cleanup(self):
        self.queue.clear()
        self.__current_battle_group = None
        self.__prev_energy = 0
        self.__current_temperature = INITIAL_TEMP
        self.__current_iteration = 0

    @property
    def currentIteration(self):
        return self.__current_iteration

    def initProcess(self):
        teams = [Team() for _ in range(TEAMS_NUM)]
        self.__current_battle_group = BattleGroup(teams)
        self.__prev_energy = self.__getEnergy(self.__current_battle_group)
        self.__current_temperature = INITIAL_TEMP
        self.__current_iteration = 0

    def enqueueDivision(self, division):
        self.queue.append(division)

        if self.logger:
            self.logger.logPlayer(division)

    def dequeueDivision(self, division):
        self.queue.remove(division)

    def processBattleGroups(self) -> Tuple:
        current_candidate = self.__generateCandidate(self.__current_battle_group)
        current_energy = self.__getEnergy(current_candidate)

        if self.logger:
            self.logger.logIteration(self.__current_iteration, self.__current_temperature, current_energy)

        if current_energy == 0:
            result_battle_group = self.__current_battle_group
            self.initProcess()
            return True, result_battle_group

        if current_energy > self.__prev_energy:
            prob = math.exp(-(current_energy - self.__prev_energy) / self.__current_temperature)
            self.logger.logProb(self.currentIteration, prob)
            if random.random() < prob:
                self.__current_battle_group = current_candidate
                self.__prev_energy = current_energy
        else:
            self.__current_battle_group = current_candidate
            self.__prev_energy = current_energy

        self.__current_iteration += 1

        if 1 < self.__current_iteration:
            self.__current_temperature = INITIAL_TEMP / math.log(1 + self.__current_iteration)

        return False, None

    def __generateCandidate(self, battle_group) -> BattleGroup:
        new_battle_group = battle_group.copy()
        actions = list(self.GENERATE_ACTIONS)
        successful = False
        while not successful and actions:
            action = actions.pop(random.randint(0, len(actions) - 1))
            successful = action(new_battle_group)

        return new_battle_group

    def swapTeamMembers(self, battle_group) -> bool:
        teams = list(battle_group.teams)
        team_1 = random.choice(teams)
        teams.remove(team_1)
        team_2 = random.choice(teams)

        if team_1.size == 0 and team_2.size == 0:
            return False

        player_team_1 = None
        if team_1.size != 0:
            player_team_1 = random.choice(team_1.divisions)
            team_1.removePlayer(player_team_1)

        player_team_2 = None
        if team_2.size != 0:
            player_team_2 = random.choice(team_2.divisions)
            team_2.removePlayer(player_team_2)

        if player_team_2 is not None:
            team_1.addPlayer(player_team_2)

        if player_team_1 is not None:
            team_2.addPlayer(player_team_1)

        return True

    def addPlayer(self, battle_group):
        if not self.queue:
            return False
        vacant_teams = [team for team in battle_group.teams if team.size < TEAM_SIZE]
        if not vacant_teams:
            return False
        vacant_team = random.choice(vacant_teams)
        vacant_team.addPlayer(self.queue.pop(0))
        return True

    def removePlayer(self, battle_group):
        teams_with_players = [
            team for team in battle_group.teams if team.size > 0]
        if not teams_with_players:
            return False
        team_with_players = random.choice(teams_with_players)
        player = random.choice(team_with_players.divisions)
        team_with_players.removePlayer(player)
        self.queue.append(player)

    @staticmethod
    def __getEnergy(battle_group):
        energy = 0
        for i, team in enumerate(battle_group.teams[:-1]):
            if team.size > 0:
                for otherTeam in battle_group.teams[i + 1:]:
                    for playerType in list(PlayerType):
                        type_num = team.playersTypesNum[playerType]
                        other_type_num = otherTeam.playersTypesNum[playerType]
                        delta_ship_type = abs(type_num - other_type_num)
                        if delta_ship_type > SHIP_TYPE_DIFFERENCE[playerType]:
                            energy += 1
                            break

            else:
                energy += (TEAMS_NUM - i - 1)

            if team.size < TEAM_SIZE:
                energy += (TEAM_SIZE - team.size)
        return energy
