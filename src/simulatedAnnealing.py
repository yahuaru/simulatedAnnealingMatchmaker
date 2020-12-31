import math
import random
from typing import Tuple

from battleGroup import Team, BattleGroup
from MatchmakerActions.addDivisionAction import AddDivisionAction
from MatchmakerActions.removeDivisionAction import RemoveDivisionAction
from MatchmakerActions.swapDivisionsAction import SwapDivisionsAction
from MatchmakerConditions import buildConditions


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


class SimulatedAnnealingMatchmaker:
    def __init__(self, params, logger=None):
        self.GENERATE_ACTIONS = [AddDivisionAction(params), RemoveDivisionAction(params), SwapDivisionsAction(params)]

        self.logger = logger

        self.__teams_num = params['teams_num']
        self.__initial_temperature = params['initial_temperature']

        self.__conditions = buildConditions(params)

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
        teams = [Team() for _ in range(self.__teams_num)]
        self.__current_battle_group = BattleGroup(teams)
        self.__prev_energy = self.__getEnergy(self.__current_battle_group)
        self.__current_temperature = self.__initial_temperature
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

    def __getEnergy(self, battle_group):
        return sum(condition.check(battle_group) for condition in self.__conditions)
