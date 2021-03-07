import random

from rules_builder.rules_director import RulesDirector
from matchmaker_queue.queue_manager import QueueManager
from collector.group_collector import GroupCollector, ProcessResult
import time

MAX_PROCESS_TIME = 0.7


class SimpleMatchmaker:
    def __init__(self, rules):
        self.__available_battle_types = []
        self._rules_collectors = {}
        queue_key_builders = {}
        for battle_type, rules_battle_type in rules.items():
            self.__available_battle_types.append(battle_type)
            self._rules_collectors[battle_type] = RulesDirector.build_rules_collector(rules_battle_type)
            queue_key_builders[battle_type] = RulesDirector.build_queue_key_builder(rules_battle_type)
        self._queue_manager = QueueManager(queue_key_builders)

    def process(self):
        battle_type = random.choice(self.__available_battle_types)
        collector = GroupCollector(self._queue_manager, battle_type, self._rules_collectors[battle_type])
        current_time = start_time = time.time()
        result, group = collector.process_battle_groups(current_time)
        process_time = time.time() - start_time
        while result == ProcessResult.NOT_COLLECTED and process_time < MAX_PROCESS_TIME:
            result, group = collector.process_battle_groups(current_time)
            process_time = time.time() - start_time
        if result != ProcessResult.COLLECTED:
            collector.cleanup()
        return group

    def enqueue_division(self, battle_type, division):
        self._queue_manager.enqueue(battle_type, division)

    def dequeue_division(self, battle_type, division):
        self._queue_manager.dequeue(battle_type, division)
