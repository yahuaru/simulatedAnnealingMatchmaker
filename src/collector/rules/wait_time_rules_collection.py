import time
from bisect import bisect
from typing import Tuple

from collector.rules.rules_collection import IRulesCollection


class WaitTimeRulesCollection(IRulesCollection):
    def __init__(self, time_intervals, rules_collections):
        assert len(time_intervals) == len(rules_collections), \
            "Wrong number of rules:{} to time:{}".format(len(rules_collections), len(time_intervals))
        self.__time_intervals = time_intervals
        self.__rules = rules_collections

    def get_state(self, battle_group) -> Tuple:
        current_rules_index = bisect(self.__time_intervals, battle_group.wait_time) - 1
        return self.__rules[current_rules_index].get_penalty(battle_group)
