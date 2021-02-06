import time
from threading import Thread

from group_collector import GroupCollector, ProcessResult

MAX_PROCESS_TIME = 0.7


class SimulatedAnnealingMatchmakerThread(Thread):
    def __init__(self, queue, group_key, params_states, on_finished):
        super().__init__()
        self.group_collector = GroupCollector(queue, group_key, params_states)
        self.__on_finished = on_finished
        self.__force_stop = None

    def run(self):
        result = ProcessResult.NOT_COLLECTED
        battle_group = None
        start_time = time.time()
        process_time = 0
        while result == ProcessResult.NOT_COLLECTED and not self.__force_stop and process_time < MAX_PROCESS_TIME:
            current_time = time.time()
            result, battle_group = self.group_collector.processBattleGroups(current_time)
            process_time = time.time() - start_time

        if result == ProcessResult.COLLECTED:
            self.__on_finished(self, True, battle_group)
        else:
            self.group_collector.cleanup()
            self.__on_finished(self, False, None)

    def stopProcessing(self):
        self.__force_stop = True
