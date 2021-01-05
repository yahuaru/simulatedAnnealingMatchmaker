import bisect
import copy
import heapq
import math
import random
from abc import ABC
from collections import namedtuple
from typing import Tuple, Optional

from battleGroup import Team, BattleGroup, Division
from MatchmakerConditions import buildConditions


class SimulatedAnnealingMatchmakerLogger(ABC):
    def cleanup(self):
        pass

    def logIteration(self, iteration, temperature, energy, probability):
        pass

    def logProb(self, iteration, prob):
        pass


SimulatedAnnealingState = namedtuple("SimulatedAnnealingState", ["temperature", "conditions", "actions"])


class SimulatedAnnealingMatchmakerQueue:
    def __init__(self, queue=None):
        self.__queue = []
        if queue is not None:
            self.__queue = sorted(queue)

    def pushDivision(self, division):
        bisect.insort(self.__queue, (division.enqueue_time, division.id, division))

    def removeDivision(self, division):
        entry = (division.enqueue_time, division.id, division)
        i = bisect.bisect_left(self.__queue, entry)
        if self.__queue[i] == entry:
            del self.__queue[i]

    def removeByIndex(self, index):
        del self.__queue[index]

    def clear(self):
        self.__queue.clear()

    def __len__(self):
        return len(self.__queue)

    def __iter__(self):
        return iter(self.__queue)


class SimulatedAnnealingMatchmaker:
    def __init__(self, params, queue=None, logger=None):
        self.logger = logger

        self.__queue = SimulatedAnnealingMatchmakerQueue(queue)

        params_by_time = list(params.items())
        params_by_time.sort(key=lambda param: param[0])

        self.__teams_num = params['teams_num']

        self.__param_state_by_time = {'time': [], 'states': []}
        common_params = copy.deepcopy(params)
        params_by_time = common_params.pop('by_time')
        for time, param in params_by_time.items():
            self.__param_state_by_time['time'].append(time)

            param.update(common_params)
            conditions, actions = buildConditions(param)
            state = SimulatedAnnealingState(param['initial_temperature'], conditions, actions)
            self.__param_state_by_time['states'].append(state)

        self.__current_battle_group = None
        self.__current_penalty = 0
        self.__current_iteration = 0

    def clear(self):
        self.__queue.clear()
        self.__param_state_by_time.clear()
        self.__current_battle_group = None
        self.__current_penalty = 0
        self.__current_iteration = 0

    @property
    def currentIteration(self):
        return self.__current_iteration

    def startProcess(self):
        teams = [Team() for _ in range(self.__teams_num)]
        self.__current_battle_group = BattleGroup(teams)

        params = self.__param_state_by_time['states'][0]
        self.__current_penalty = self.__getPenalty(self.__current_battle_group, params.conditions)

        self.__current_iteration = 0

    def stopProcess(self):
        for team in self.__current_battle_group:
            for division in team.divisions:
                self.__queue.pushDivision(division)
        self.__current_battle_group = None
        self.__current_penalty = 0
        self.__current_iteration = 0

    def enqueueDivision(self, division):
        self.__queue.pushDivision(division)

    def dequeueDivision(self, division):
        self.__queue.removeDivision(division)

    def processBattleGroups(self, current_time) -> Tuple:
        current_wait_time = current_time - self.__current_battle_group.min_enqueue_time
        current_param_index = bisect.bisect(self.__param_state_by_time['time'], current_wait_time) - 1
        current_actions = self.__param_state_by_time['states'][current_param_index].actions

        candidate, applied_action = self.__generateCandidate(self.__current_battle_group, current_actions)
        current_candidate_wait_time = current_time - candidate.min_enqueue_time
        candidate_param_index = bisect.bisect(self.__param_state_by_time['time'], current_candidate_wait_time) - 1
        candidate_param = self.__param_state_by_time['states'][candidate_param_index]
        candidate_penalty = self.__getPenalty(candidate, candidate_param.conditions)

        if candidate_penalty == 0:
            self.__acceptCandidate(candidate, candidate_penalty, applied_action)
            return True, candidate

        if candidate_penalty > self.__current_penalty:
            current_temperature = candidate_param.temperature
            if self.__current_iteration > 0:
                current_temperature = candidate_param.temperature / math.log(1 + self.__current_iteration)

            probability = math.exp(-(candidate_penalty - self.__current_penalty) / current_temperature)

            if random.random() < probability:
                self.__acceptCandidate(candidate, candidate_penalty, applied_action)
            else:
                self.__rejectCandidate(applied_action)

            if self.logger:
                self.logger.logIteration(self.__current_iteration, current_temperature, candidate_penalty, probability)
        else:
            self.__acceptCandidate(candidate, candidate_penalty, applied_action)

            if self.logger:
                current_temperature = candidate_param.temperature
                if self.__current_iteration > 0:
                    current_temperature = candidate_param.temperature / math.log(1 + self.__current_iteration)
                probability = math.exp(-(candidate_penalty - self.__current_penalty) / current_temperature)
                self.logger.logIteration(self.__current_iteration, current_temperature, candidate_penalty, probability)

        self.__current_iteration += 1

        return False, None

    def __acceptCandidate(self, candidate, prev_penalty, applied_action):
        self.__current_battle_group = candidate
        self.__current_penalty = prev_penalty
        applied_action.on_approved(self.__queue)
        total_sum = sum(team.size for team in self.__current_battle_group.teams) + sum(division.size for _, _, division in self.__queue)
        assert total_sum == 9


    def __rejectCandidate(self, applied_action):
        applied_action.on_rejected(self.__queue)

        total_sum = sum(team.size for team in self.__current_battle_group.teams) + sum(division.size for _, _, division in self.__queue)

        assert total_sum == 9


    def __generateCandidate(self, battle_group, generate_actions) -> Tuple:
        actions = list(generate_actions)
        successful = False
        action = None
        new_battle_group = None
        while not successful:
            action = actions.pop(random.randint(0, len(actions) - 1))
            new_battle_group = battle_group.copy()
            successful = action.execute(self.__queue, new_battle_group)

        return new_battle_group, action

    @staticmethod
    def __getPenalty(battle_group, penalty_conditions):
        return sum(condition.check(battle_group) for condition in penalty_conditions)
