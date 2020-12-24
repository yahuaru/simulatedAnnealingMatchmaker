import math
import random
from typing import Tuple

from MatchmakerConditions import (SHIP_TYPE_DIFFERENCE, TEAM_SIZE, TEAMS_NUM,
                                  BattleGroup, Team, MAX_LEVEL_DIFFERENCE)
from player import PlayerType

TEMP_DECREASE_COEFFICIENT = 0.7


class SimulatedAnnealingMatchmakerLogger:
    def __init__(self):
        self.iterations = []
        self.prob = []

    def cleanup(self):
        self.iterations = []
        self.prob = []

    def logIteration(self, iteration, temperature, energy):
        self.iterations.append((iteration, temperature, energy))

    def logProb(self, iteration, prob):
        self.prob.append((iteration, prob))


class SimulatedAnnealingAction:

    def execute(self, queue, battle_group):
        pass

    def on_approved(self, queue):
        pass

    def on_rejected(self, queue):
        pass


class AddDivisionAction(SimulatedAnnealingAction):

    def __init__(self):
        self.__added_division = None

    def execute(self, queue, battle_group):
        if not queue:
            return False
        vacant_teams = [team for team in battle_group.teams if team.size < TEAM_SIZE]
        if not vacant_teams:
            return False

        vacant_team = random.choice(vacant_teams)
        acceptable_division = None
        for division in queue:
            if division.size <= (TEAM_SIZE - vacant_team.size):
                acceptable_division = division
                break
        if acceptable_division is None:
            return False
        self.__added_division = acceptable_division
        queue.remove(self.__added_division)
        vacant_team.addDivision(self.__added_division)
        return True

    def on_approved(self, queue):
        self.__added_division = None

    def on_rejected(self, queue):
        queue.append(self.__added_division)
        self.__added_division = None


class RemoveDivisionAction(SimulatedAnnealingAction):
    def __init__(self):
        self.__removed_division = None

    def execute(self, queue, battle_group):
        not_empty_team = [team for team in battle_group.teams if team.size > 0]
        if not not_empty_team:
            return False

        team = random.choice(not_empty_team)
        division = random.choice(team.divisions)
        team.removeDivision(division)
        self.__removed_division = division
        return True

    def on_approved(self, queue):
        queue.append(self.__removed_division)
        self.__removed_division = None

    def on_rejected(self, queue):
        self.__removed_division = None


class SwapDivisionsAction(SimulatedAnnealingAction):
    def execute(self, queue, battle_group):
        teams = list(battle_group.teams)
        team = random.choice(teams)
        teams.remove(team)
        other_team = random.choice(teams)

        if team.size == 0 and other_team.size == 0:
            return False

        division = None
        if team.size != 0:
            division = random.choice(team.divisions)

        other_division = None
        if other_team.size != 0:
            other_division = random.choice(other_team.divisions)

        if division is not None and other_division is not None:
            if (division.size <= (other_division.size + TEAM_SIZE - other_team.size)
                    and other_division.size <= (division.size + TEAM_SIZE - team.size)):
                other_team.removeDivision(other_division)
                team.removeDivision(division)

                other_team.addDivision(division)
                team.addDivision(other_division)
                return True
        elif division is not None:
            team.addDivision(division)
            other_team.addDivision(division)
            return True
        elif other_division is not None and (TEAM_SIZE - team.size) <= other_division.size:
            other_team.removeDivision(other_division)
            team.addDivision(other_division)
            return True

        return False


class SimulatedAnnealingMatchmaker:
    def __init__(self, logger=None):
        self.__initial_temperature = 0
        self.GENERATE_ACTIONS = [AddDivisionAction(), RemoveDivisionAction(), SwapDivisionsAction()]

        self.logger = logger

        self.queue = []
        self.__current_battle_group = None
        self.__current_temperature = 0
        self.__prev_energy = 0
        self.__current_iteration = 0
        self.__last_action = None

        self.initProcess()

    def cleanup(self):
        self.queue.clear()
        self.__current_battle_group = None
        self.__prev_energy = 0
        self.__current_temperature = 0
        self.__current_iteration = 0
        self.__last_action = None

    @property
    def currentIteration(self):
        return self.__current_iteration

    def initProcess(self):
        teams = [Team() for _ in range(TEAMS_NUM)]
        self.__current_battle_group = BattleGroup(teams)
        self.__prev_energy = self.__getEnergy(self.__current_battle_group)
        self.__initial_temperature = self.__prev_energy
        self.__current_temperature = self.__prev_energy
        self.__current_iteration = 0
        self.__last_action = None

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
            self.__last_action.on_approved(self.queue)
            return True, current_candidate

        if current_energy > self.__prev_energy:
            prob = math.exp(-(current_energy - self.__prev_energy) / self.__current_temperature)

            if self.logger:
                self.logger.logProb(self.currentIteration, prob)

            if random.random() < prob:
                self.__current_battle_group = current_candidate
                self.__prev_energy = current_energy
                self.__last_action.on_approved(self.queue)
            else:
                self.__last_action.on_rejected(self.queue)
        else:
            if self.logger:
                self.logger.logProb(self.currentIteration, 1.0)

            self.__current_battle_group = current_candidate
            self.__prev_energy = current_energy
            self.__last_action.on_approved(self.queue)

        self.__current_iteration += 1

        if 1 < self.__current_iteration:
            self.__current_temperature = self.__initial_temperature / math.log(1 + self.__current_iteration)

        return False, None

    def __generateCandidate(self, battle_group) -> BattleGroup:
        actions = list(self.GENERATE_ACTIONS)
        successful = False
        action = None
        new_battle_group = None
        while not successful:
            action = actions.pop(random.randint(0, len(actions) - 1))
            new_battle_group = battle_group.copy()
            successful = action.execute(self.queue, new_battle_group)

        if successful:
            self.__last_action = action

        return new_battle_group

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
