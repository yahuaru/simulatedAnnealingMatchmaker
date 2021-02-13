from group_rules import BattleRules
from matchmaker_queue.queue_manager import QueueManager
from group_collector import GroupCollector, ProcessResult
import time

MAX_PROCESS_TIME = 0.7


class SimpleMatchmaker:
    def __init__(self, params):
        self.__queue_manager = QueueManager(params)

        self.__param_by_battle_type = {}
        for battle_type, battle_type_params in params.items():
            self.__param_by_battle_type[battle_type] = BattleRules(params[battle_type])

    def process(self):
        key = self.__queue_manager.get_next_available_group_key()
        collector = GroupCollector(self.__queue_manager, key, self.__param_by_battle_type[key.battle_type])
        current_time = start_time = time.time()
        result, group = collector.processBattleGroups(current_time)
        process_time = time.time() - start_time
        while result == ProcessResult.NOT_COLLECTED and process_time < MAX_PROCESS_TIME:
            current_time = time.time()
            result, group = collector.processBattleGroups(current_time)
            process_time = time.time() - start_time
        if result != ProcessResult.COLLECTED:
            collector.cleanup()
        self.__queue_manager.push_key(key)
        return group

    def enqueueDivision(self, battle_type, division):
        self.__queue_manager.enqueue(battle_type, division)

    def dequeueDivision(self, battle_type, division):
        self.__queue_manager.dequeue(battle_type, division)

