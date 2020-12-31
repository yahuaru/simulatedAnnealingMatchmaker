import math
import random
from abc import ABC
from typing import Tuple

from battleGroup import Team, BattleGroup
from MatchmakerConditions import buildConditions


class SimulatedAnnealingMatchmakerLogger(ABC):
    def cleanup(self):
        pass

    def logIteration(self, iteration, temperature, energy, probability):
        pass

    def logProb(self, iteration, prob):
        pass


class SimulatedAnnealingMatchmaker:
    def __init__(self, params, logger=None):
        self.logger = logger

        self.__teams_num = params['teams_num']
        self.__initial_temperature = params['initial_temperature']

        self.__conditions, actions = buildConditions(params)
        self.__actions = [action(params) for action in actions]

        self.queue = []
        self.__current_battle_group = None
        self.__current_temperature = 0
        self.__prev_penalty = 0
        self.__current_iteration = 0
        self.__last_action = None

    def cleanup(self):
        self.queue.clear()
        self.__current_battle_group = None
        self.__prev_penalty = 0
        self.__current_temperature = 0
        self.__current_iteration = 0
        self.__last_action = None

    @property
    def currentIteration(self):
        return self.__current_iteration

    def startProcess(self):
        teams = [Team() for _ in range(self.__teams_num)]
        self.__current_battle_group = BattleGroup(teams)
        self.__prev_penalty = self.__getPenalty(self.__current_battle_group)
        self.__current_temperature = self.__initial_temperature
        self.__current_iteration = 0
        self.__last_action = None

    def stopProcess(self):
        for team in self.__current_battle_group:
            for division in team.divisions:
                self.queue.append(division)
        self.__current_battle_group = None
        self.__prev_penalty = 0
        self.__current_temperature = 0
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
        current_penalty = self.__getPenalty(current_candidate)

        if current_penalty == 0:
            self.__last_action.on_approved(self.queue)
            return True, current_candidate

        if current_penalty > self.__prev_penalty:
            probability = math.exp(-(current_penalty - self.__prev_penalty) / self.__current_temperature)

            if self.logger:
                self.logger.logIteration(self.__current_iteration, self.__current_temperature, current_penalty,
                                         probability)

            if random.random() < probability:
                self.__current_battle_group = current_candidate
                self.__prev_penalty = current_penalty
                self.__last_action.on_approved(self.queue)
            else:
                self.__last_action.on_rejected(self.queue)
        else:
            if self.logger:
                self.logger.logIteration(self.__current_iteration, self.__current_temperature, current_penalty, 1.0)

            self.__current_battle_group = current_candidate
            self.__prev_penalty = current_penalty
            self.__last_action.on_approved(self.queue)

        self.__current_iteration += 1

        if 1 < self.__current_iteration:
            self.__current_temperature = self.__initial_temperature / math.log(1 + self.__current_iteration)

        return False, None

    def __generateCandidate(self, battle_group) -> BattleGroup:
        actions = list(self.__actions)
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

    def __getPenalty(self, battle_group):
        return sum(condition.check(battle_group) for condition in self.__conditions)
