import bisect
import math
import random
import time
from enum import Enum, IntEnum, auto
from threading import Thread
from typing import Tuple

from battleGroup import Team, BattleGroup

MAX_PROCESS_TIME = 0.7


class ProcessResult(IntEnum):
    COLLECTED = auto()
    NOT_COLLECTED = auto()
    NO_ACTIONS = auto()


class SimulatedAnnealingMatchmakerThread(Thread):
    def __init__(self, queue, params_states, on_finished):
        super().__init__()

        self.__queue = queue
        self.__on_finished = on_finished

        self.__current_battle_group = None
        self.__current_penalty = 0
        self.__current_iteration = 0
        self.__param_state_by_time = params_states
        self.__start_time = 0

        self.__force_stop = False

    def startProcessing(self, teams_num):
        teams = [Team() for _ in range(teams_num)]
        self.__current_battle_group = BattleGroup(teams)

        initial_conditions = self.__param_state_by_time['states'][0].conditions
        self.__current_penalty = self.__getPenalty(self.__current_battle_group, initial_conditions)

        self.__current_iteration = 0

        self.__start_time = time.time()
        self.start()

    def run(self) -> None:
        result = ProcessResult.NOT_COLLECTED
        battle_group = None
        process_time = time.time() - self.__start_time
        while result == ProcessResult.NOT_COLLECTED and not self.__force_stop and process_time < MAX_PROCESS_TIME:
            result, battle_group = self.__processBattleGroups(time.time())
            process_time = time.time() - self.__start_time

        if result == ProcessResult.COLLECTED:
            self.__current_battle_group = None
            self.__on_finished(self, True, battle_group)
        else:
            for team in self.__current_battle_group.teams:
                for division in team.divisions:
                    self.__queue.pushDivision(division)
            self.__current_battle_group = None
            self.__on_finished(self, False, None)

    def stopProcessing(self):
        self.__force_stop = True

    def __processBattleGroups(self, current_time):
        current_wait_time = current_time - self.__current_battle_group.min_enqueue_time
        current_param_index = bisect.bisect(self.__param_state_by_time['time'], current_wait_time) - 1
        current_actions = self.__param_state_by_time['states'][current_param_index].actions
        current_conditions_param = self.__param_state_by_time['states'][current_param_index].conditions_param

        successful, candidate, applied_action = self.__generateCandidate(self.__current_battle_group,
                                                                         current_conditions_param, current_actions)
        if not successful:
            return ProcessResult.NO_ACTIONS, None

        current_candidate_wait_time = current_time - candidate.min_enqueue_time
        candidate_param_index = bisect.bisect(self.__param_state_by_time['time'], current_candidate_wait_time) - 1
        candidate_param = self.__param_state_by_time['states'][candidate_param_index]
        candidate_penalty = self.__getPenalty(candidate, candidate_param.conditions)

        if candidate_penalty == 0:
            self.__acceptCandidate(candidate, candidate_penalty, applied_action)
            return ProcessResult.COLLECTED, candidate

        if candidate_penalty > self.__current_penalty:
            current_temperature = candidate_param.temperature
            if self.__current_iteration > 0:
                current_temperature = candidate_param.temperature / math.log(1 + self.__current_iteration)

            probability = math.exp(-(candidate_penalty - self.__current_penalty) / current_temperature)

            if random.random() < probability:
                self.__acceptCandidate(candidate, candidate_penalty, applied_action)
            else:
                self.__rejectCandidate(applied_action)
        else:
            self.__acceptCandidate(candidate, candidate_penalty, applied_action)

        self.__current_iteration += 1

        return ProcessResult.NOT_COLLECTED, None

    def __acceptCandidate(self, candidate, prev_penalty, applied_action):
        self.__current_battle_group = candidate
        self.__current_penalty = prev_penalty
        applied_action.on_approved(self.__queue)

    def __rejectCandidate(self, applied_action):
        applied_action.on_rejected(self.__queue)

    def __generateCandidate(self, battle_group, params, generate_actions) -> Tuple:
        actions = list(generate_actions)
        successful = False
        action = None
        new_battle_group = None
        while not successful and actions:
            action_class = actions.pop(random.randint(0, len(actions) - 1))
            action = action_class(params)
            new_battle_group = battle_group.copy()
            successful = action.execute(self.__queue, new_battle_group)

        if not successful:
            return False, None, None

        return successful, new_battle_group, action

    @staticmethod
    def __getPenalty(battle_group, penalty_conditions):
        return sum(condition.check(battle_group) for condition in penalty_conditions)