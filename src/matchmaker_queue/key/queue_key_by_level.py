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

    def get_group_keys(self, division) -> List:
        min_level_key = max(division.max_level, self._min_level + self._max_level_difference)
        max_level_key = min(division.max_level + self._max_level_difference,
                            self._max_level - self._max_level_difference)
        return [i for i in range(min_level_key, max_level_key + 1)]