from group_rules import BattleRules
from matchmaker_queue.queue_manager import QueueManager
from group_collector import GroupCollector
from simulatedAnnealingThread import SimulatedAnnealingMatchmakerThread


class MatchmakerThreadBuilder(object):
    def __init__(self, params):
        self.__param_by_battle_type = {}
        for battle_type, battle_type_params in params.items():
            self.__param_by_battle_type[battle_type] = BattleRules(params[battle_type])

    def build_thread(self, queue, group_key, on_thread_finished):
        thread_params = self.__param_by_battle_type[group_key.battle_type]
        return SimulatedAnnealingMatchmakerThread(queue, group_key, thread_params, on_thread_finished)


class SimulatedAnnealingMatchmaker:
    def __init__(self, params, threads_num, on_battle_group_collected):
        self.__queue_manager = QueueManager(params)
        self.__thread_builder = MatchmakerThreadBuilder(params)

        self.__threads_num = threads_num
        self.__on_battle_group_collected = on_battle_group_collected

        self.__is_processing = False

        self.__threads = []

    def __on_thread_finished(self, thread, is_successful, battle_group):
        if is_successful:
            self.__on_battle_group_collected(battle_group)
        self.__threads.remove(thread)

    def startProcess(self):
        for i in range(len(self.__threads), self.__threads_num):
            group_key = self.__queue_manager.get_next_available_group_key()
            if group_key is None:
                break
            thread = self.__thread_builder.build_thread(self.__queue_manager, group_key, self.__on_thread_finished)
            self.__threads.append(thread)
            thread.start()

    def waitForCompletion(self):
        for thread in self.__threads:
            if thread.is_alive():
                thread.join()

    def stopProcess(self):
        for thread in self.__threads:
            if thread.is_alive():
                thread.stopProcessing()
                thread.join()

    def enqueueDivision(self, battle_type, division):
        self.__queue_manager.enqueue(battle_type, division)

    def dequeueDivision(self, battle_type, division):
        self.__queue_manager.dequeue(battle_type, division)

    @staticmethod
    def __getPenalty(battle_group, penalty_conditions):
        return sum(condition.check(battle_group) for condition in penalty_conditions)
