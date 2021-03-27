import logging
import math
import random
from enum import IntEnum, auto
from typing import Tuple

from battle_group.battle_group import BattleGroup
from collector.actions import random_actions_generator


class ProcessResult(IntEnum):
    COLLECTED = 1
    NOT_COLLECTED = 2
    NO_ACTIONS = 3


class GroupCollector:
    def __init__(self, queue, battle_type, rules_collection):
        self._battle_type = battle_type
        self._queue = queue

        self.__rules_collection = rules_collection

        self.__current_iteration = 0
        self.__battle_group = BattleGroup()
        self.__current_state = self.__rules_collection.get_state(self.__battle_group)

    def cleanup(self):
        for team in self.__battle_group.teams:
            for division in team.divisions:
                self._queue.enqueue(self._battle_type, division)

    def process_battle_groups(self, current_time):
        candidate, applied_action = self.__generate_candidate(current_time, self.__battle_group, self.__current_state.rules)
        if candidate is None:
            return ProcessResult.NO_ACTIONS, None

        candidate_state = self.__rules_collection.get_state(candidate)

        if candidate_state.penalty == 0:
            self.__accept_candidate(candidate, candidate_state, applied_action)
            return ProcessResult.COLLECTED, candidate

        if candidate_state.penalty > self.__current_state.penalty:
            current_temperature = candidate_state.temperature
            if self.__current_iteration > 0:
                current_temperature = candidate_state.temperature / math.log(1 + self.__current_iteration)

            probability = math.exp(-(candidate_state.penalty - self.__current_state.penalty) / current_temperature)
            if random.random() < probability:
                self.__accept_candidate(candidate, candidate_state, applied_action)
            else:
                self.__reject_candidate(applied_action)
        else:
            self.__accept_candidate(candidate, candidate_state, applied_action)

        self.__current_iteration += 1

        return ProcessResult.NOT_COLLECTED, None

    def __accept_candidate(self, candidate, candidate_state, applied_action):
        self.__current_state = candidate_state
        self.__battle_group = candidate
        applied_action.on_approved(self._queue, self._battle_type)

    def __reject_candidate(self, applied_action):
        applied_action.on_rejected(self._queue, self._battle_type)

    def __generate_candidate(self, current_time, battle_group, rules) -> Tuple:
        for action in random_actions_generator(rules):
            new_battle_group = action.execute(current_time, self._queue, self._battle_type, battle_group)
            if new_battle_group is not None:
                return new_battle_group, action

        return None, None
