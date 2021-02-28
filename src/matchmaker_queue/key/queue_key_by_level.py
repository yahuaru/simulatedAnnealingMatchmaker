import sys
from typing import List

from matchmaker_queue.key.queue_key_generator import IQueueKeyGenerator


class QueueKeyByLevel(IQueueKeyGenerator):
    REQUIRED_FIELDS = {"by_level", }

    def __init__(self, params):
        super().__init__(params)
        by_level_rules = params['common_conditions']['by_level']
        self._max_level_difference = by_level_rules['max_level_difference']
        self._min_level = by_level_rules['min_level']
        self._max_level = by_level_rules['max_level']

    def get_key(self, division) -> List:
        return division.max_level

    def get_available_keys(self, battle_group) -> List:
        if battle_group.isEmpty():
            return list(range(self._min_level, self._max_level + 1))

        max_level = 0
        min_level = sys.maxsize
        for team in battle_group.teams:
            for division in team.divisions:
                max_level = max(division.max_level, max_level)
                min_level = min(division.max_level, min_level)
        max_level_key = min(min_level + self._max_level_difference, self._max_level)
        min_level_key = max(max_level - self._max_level_difference, self._min_level)
        return list(range(min_level_key, max_level_key + 1))
