import bisect
import logging
import math
import random
import threading
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
    def __init__(self, queue_entry, params_states, on_finished):
        super().__init__()

        self._queue_entry = queue_entry
        self._queue = queue_entry.queue
        self.__on_finished = on_finished

        self.__current_battle_group = None
        self.__current_penalty = 0
        self.__current_iteration = 0
        self.__params_states = params_states

        self.__force_stop = False

    def startProcessing(self):
        team_num = self.__params_states._teams_num
        teams = [Team() for _ in range(team_num)]
        self.__current_battle_group = BattleGroup(teams)

        initial_state = self.__params_states.get_state_by_time(0)
        initial_conditions = initial_state.conditions
        self.__current_penalty = self.__getPenalty(self.__current_battle_group, initial_conditions)

        self.__current_iteration = 0

        self.start()

    def run(self) -> None:
        result = ProcessResult.NOT_COLLECTED
        battle_group = None
        start_time = time.time()
        process_time = 0
        while result == ProcessResult.NOT_COLLECTED and not self.__force_stop and process_time < MAX_PROCESS_TIME:
            current_time = time.time()
            result, battle_group = self.__processBattleGroups(current_time)
            process_time = time.time() - start_time

        if result == ProcessResult.COLLECTED:
            self.__current_battle_group = None
            self.__on_finished(self, True, battle_group)
        else:
            for team in self.__current_battle_group.teams:
                for division in team.divisions:
                    self._queue.enqueue(division)
            self.__current_battle_group = None
            self.__on_finished(self, False, None)

    def stopProcessing(self):
        self.__force_stop = True

    def __processBattleGroups(self, current_time):
        if self.__current_battle_group.isEmpty():
            current_wait_time = 0
        else:
            current_wait_time = current_time - self.__current_battle_group.min_enqueue_time

        current_rules = self.__params_states.get_state_by_time(current_wait_time)
        current_actions = current_rules.actions
        current_conditions_param = current_rules.conditions_param

        candidate, applied_action = self.__generateCandidate(self.__current_battle_group, current_conditions_param,
                                                             current_actions)
        if candidate is None:
            return ProcessResult.NO_ACTIONS, None
        elif candidate.isEmpty():
            return ProcessResult.NOT_COLLECTED, None

        current_candidate_wait_time = current_time - candidate.min_enqueue_time
        candidate_rules = self.__params_states.get_state_by_time(current_candidate_wait_time)
        candidate_penalty = self.__getPenalty(candidate, candidate_rules.conditions)

        if candidate_penalty == 0:
            self.__acceptCandidate(candidate, candidate_penalty, applied_action)
            return ProcessResult.COLLECTED, candidate

        if candidate_penalty > self.__current_penalty:
            current_temperature = candidate_rules.temperature
            if self.__current_iteration > 0:
                current_temperature = candidate_rules.temperature / math.log(1 + self.__current_iteration)

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
        logging.debug("action approved Action:{} Thread:{}".format(applied_action.__class__, threading.get_ident()))
        self.__current_battle_group = candidate
        self.__current_penalty = prev_penalty
        applied_action.on_approved(self._queue)

    def __rejectCandidate(self, applied_action):
        logging.debug("action rejected Action:{} Thread:{}".format(applied_action.__class__, threading.get_ident()))
        applied_action.on_rejected(self._queue)

    def __generateCandidate(self, battle_group, params, generate_actions) -> Tuple:
        actions = list(generate_actions)
        action = None
        new_battle_group = None
        while new_battle_group is None and actions:
            action_class = actions.pop(random.randint(0, len(actions) - 1))
            action = action_class(params)
            new_battle_group = action.execute(self._queue, battle_group)

        return new_battle_group, action

    @staticmethod
    def __getPenalty(battle_group, penalty_conditions):
        return sum(condition.check(battle_group) for condition in penalty_conditions)