import random

from battle_rules import BattleRules
from matchmaker_queue.queue_manager import QueueManager
from collector.group_collector import GroupCollector, ProcessResult
import time

MAX_PROCESS_TIME = 0.7


class SimpleMatchmaker:
    def __init__(self, params):
        self.__queue_manager = QueueManager(params)

        self.__available_battle_types = []
        self.__param_by_battle_type = {}
        for battle_type, battle_type_params in params.items():
            self.__available_battle_types.append(battle_type)
            self.__param_by_battle_type[battle_type] = BattleRules(params[battle_type])

    def process(self):
        battle_type = random.choice(self.__available_battle_types)
        collector = GroupCollector(self.__queue_manager, battle_type, self.__param_by_battle_type[battle_type])
        current_time = start_time = time.time()
        result, group = collector.processBattleGroups(current_time)
        process_time = time.time() - start_time
        while result == ProcessResult.NOT_COLLECTED and process_time < MAX_PROCESS_TIME:
            current_time = time.time()
            result, group = collector.processBattleGroups(current_time)
            process_time = time.time() - start_time
        if result != ProcessResult.COLLECTED:
            collector.cleanup()
        return group

    def enqueueDivision(self, battle_type, division):
        self.__queue_manager.enqueue(battle_type, division)

    def dequeueDivision(self, battle_type, division):
        self.__queue_manager.dequeue(battle_type, division)

