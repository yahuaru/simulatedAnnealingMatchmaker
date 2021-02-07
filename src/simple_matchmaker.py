from group_rules import BattleRules
from matchmaker_queue.queue_manager import QueueManager
from group_collector import GroupCollector, ProcessResult
from time import time

class MatchmakerThreadBuilder(object):
    def __init__(self, params):
        self.__param_by_battle_type = {}
        for battle_type, battle_type_params in params.items():
            self.__param_by_battle_type[battle_type] = BattleRules(params[battle_type])

    def build_thread(self, queue, group_key, on_thread_finished):
        thread_params = self.__param_by_battle_type[group_key.battle_type]
        return GroupCollector(queue, group_key, thread_params)


class SimpleMatchmaker:
    def __init__(self, params):
        self.__queue_manager = QueueManager(params)

        self.__param_by_battle_type = {}
        for battle_type, battle_type_params in params.items():
            self.__param_by_battle_type[battle_type] = BattleRules(params[battle_type])

    def process(self):
        key = self.__queue_manager.get_next_available_group_key()
        collector = GroupCollector(self.__queue_manager, key, self.__param_by_battle_type[key.battle_type])
        current_time = time()
        result, group = collector.processBattleGroups(current_time)
        while result == ProcessResult.NOT_COLLECTED:
            result, group = collector.processBattleGroups(current_time)
        if result == ProcessResult.NOT_COLLECTED:
            collector.cleanup()
        return group

    def enqueueDivision(self, battle_type, division):
        self.__queue_manager.enqueue(battle_type, division)

    def dequeueDivision(self, battle_type, division):
        self.__queue_manager.dequeue(battle_type, division)

