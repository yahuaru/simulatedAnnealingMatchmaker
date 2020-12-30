import math
import random
from abc import ABC
from typing import Tuple

from battleGroup import Team, BattleGroup
from MatchmakerActions.addDivisionAction import AddDivisionAction
from MatchmakerActions.removeDivisionAction import RemoveDivisionAction
from MatchmakerActions.swapDivisionsAction import SwapDivisionsAction
from MatchmakerConditions import buildConditions


class SimulatedAnnealingMatchmakerLogger(ABC):
    def __init__(self):
        pass

    def cleanup(self):
        pass

    def logIteration(self, iteration, temperature, energy, prob):
        pass


class SimulatedAnnealingMatchmaker:
    def __init__(self, params, logger=None):
        self.logger = logger

        self.__teams_num = params['teams_num']
        self.__initial_temperature = params['initial_temperature']

        self.__conditions, self.__available_actions = buildConditions(params)
        self.__actions_instances = {action: action(params) for action in self.__available_actions}

        self.queue = []
        self.__current_battle_group = None
        self.__current_temperature = 0
        self.__prev_energy = 0
        self.__prev_actions_weights = ()
        self.__current_iteration = 0
        self.__last_action = None

    def cleanup(self):
        self.queue.clear()
        self.__prev_actions_weights = ()
        self.__current_battle_group = None
        self.__prev_energy = 0
        self.__current_temperature = 0
        self.__current_iteration = 0
        self.__last_action = None

    @property
    def currentIteration(self):
        return self.__current_iteration

    def startProcess(self):
        teams = [Team() for _ in range(self.__teams_num)]
        self.__current_battle_group = BattleGroup(teams)
        self.__prev_energy, self.__prev_actions_weights = self.__getEnergy(self.__current_battle_group)
        self.__current_temperature = self.__initial_temperature
        self.__current_iteration = 0
        self.__last_action = None

    def stopProcess(self):
        for team in self.__current_battle_group.teams:
            for division in team.divisions:
                self.queue.append(division)
        self.__current_battle_group = None
        self.__prev_energy = 0
        self.__prev_actions_weights = ()
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
        current_energy, current_actions_weights = self.__getEnergy(current_candidate)

        if current_energy == 0:
            self.__last_action.on_approved(self.queue)
            return True, current_candidate

        probability = 1.0
        if current_energy > self.__prev_energy:
            probability = math.exp(-(current_energy - self.__prev_energy) / self.__current_temperature)

        if self.logger is not None:
            self.logger.logIteration(self.__current_iteration, self.__current_temperature, current_energy, probability)

        if probability >= 1.0 or random.random() < probability:
            self.__current_battle_group = current_candidate
            self.__prev_energy = current_energy
            self.__prev_actions_weights = current_actions_weights

            self.__last_action.on_approved(self.queue)
        else:
            self.__last_action.on_rejected(self.queue)

        self.__current_iteration += 1

        if 1 < self.__current_iteration:
            self.__current_temperature = self.__initial_temperature / math.log(1 + self.__current_iteration)

        return False, None

    def __generateCandidate(self, battle_group) -> BattleGroup:
        successful = False
        new_battle_group = None
        actions_weights = list(self.__prev_actions_weights)
        action_instance = None
        while not successful:
            max_weight = max(action_weight[1] for action_weight in actions_weights)
            probability = random.random() * max_weight
            current_action = None
            for action_weight in actions_weights:
                if probability < action_weight[1]:
                    current_action = action_weight
                    break

            new_battle_group = battle_group.copy()
            action_instance = self.__actions_instances[current_action[0]]
            successful = action_instance.execute(self.queue, new_battle_group)
            if not successful:
                actions_weights.remove(current_action)

        if successful:
            self.__last_action = action_instance

        return new_battle_group

    def __getEnergy(self, battle_group):
        actions_weights = {action: 0 for action in self.__available_actions}
        total_penalty = 0
        for condition in self.__conditions:
            penalty = condition.check(battle_group)
            total_penalty += penalty
            for action in condition.ACTIONS:
                actions_weights[action] += penalty

        actions_weights = ((action, weight) for action, weight in actions_weights.items())
        actions_weights = sorted(actions_weights, key=lambda v: v[1])

        return total_penalty, actions_weights
