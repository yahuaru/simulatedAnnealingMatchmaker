import logging
import math
import random
from enum import IntEnum, auto
from typing import Tuple

from battle_group import Team, BattleGroup


class ProcessResult(IntEnum):
    COLLECTED = auto()
    NOT_COLLECTED = auto()
    NO_ACTIONS = auto()


class GroupCollector:
    def __init__(self, queue, battle_type, params_states):
        self._battle_type = battle_type
        self._queue = queue

        self.__params_states = params_states

        self.__current_iteration = 0

        team_num = self.__params_states.teams_num
        teams = [Team() for _ in range(team_num)]
        self.__current_battle_group = BattleGroup(teams)

        initial_state = self.__params_states.get_state_by_time(0)
        initial_conditions = initial_state.conditions
        self.__current_penalty = self.__get_penalty(self.__current_battle_group, initial_conditions)

    def cleanup(self):
        for team in self.__current_battle_group.teams:
            for division in team.divisions:
                self._queue.enqueue(self._battle_type, division)
        self.__current_battle_group = None
        return False, None

    def process_battle_groups(self, current_time):
        if self.__current_battle_group.is_empty():
            current_wait_time = 0
        else:
            current_wait_time = current_time - self.__current_battle_group.min_enqueue_time

        current_rules = self.__params_states.get_state_by_time(current_wait_time)
        current_actions = current_rules.actions
        current_conditions_param = current_rules.conditions_param

        candidate, applied_action = self.__generate_candidate(self.__current_battle_group, current_conditions_param,
                                                              current_actions)
        if candidate is None:
            return ProcessResult.NO_ACTIONS, None
        elif candidate.is_empty():
            return ProcessResult.NOT_COLLECTED, None

        current_candidate_wait_time = current_time - candidate.min_enqueue_time
        candidate_rules = self.__params_states.get_state_by_time(current_candidate_wait_time)
        candidate_penalty = self.__get_penalty(candidate, candidate_rules.conditions)

        if candidate_penalty == 0:
            self.__accept_candidate(candidate, candidate_penalty, applied_action)
            return ProcessResult.COLLECTED, candidate

        if candidate_penalty > self.__current_penalty:
            current_temperature = candidate_rules.temperature
            if self.__current_iteration > 0:
                current_temperature = candidate_rules.temperature / math.log(1 + self.__current_iteration)

            probability = math.exp(-(candidate_penalty - self.__current_penalty) / current_temperature)
            if random.random() < probability:
                self.__accept_candidate(candidate, candidate_penalty, applied_action)
            else:
                self.__reject_candidate(applied_action)
        else:
            self.__accept_candidate(candidate, candidate_penalty, applied_action)

        self.__current_iteration += 1

        return ProcessResult.NOT_COLLECTED, None

    def __accept_candidate(self, candidate, prev_penalty, applied_action):
        logging.debug("action approved Action:{}".format(applied_action.__class__))
        self.__current_battle_group = candidate
        self.__current_penalty = prev_penalty
        applied_action.on_approved(self._queue, self._battle_type)

    def __reject_candidate(self, applied_action):
        logging.debug("action rejected Action:{}".format(applied_action.__class__))
        applied_action.on_rejected(self._queue, self._battle_type)

    def __generate_candidate(self, battle_group, params, generate_actions) -> Tuple:
        actions = list(generate_actions)
        action = None
        new_battle_group = None
        while new_battle_group is None and actions:
            action_class = actions.pop(random.randint(0, len(actions) - 1))
            action = action_class(params)
            new_battle_group = action.execute(self._queue, self._battle_type, battle_group)

        return new_battle_group, action

    @staticmethod
    def __get_penalty(battle_group, penalty_conditions):
        return sum(condition.check(battle_group) for condition in penalty_conditions)
