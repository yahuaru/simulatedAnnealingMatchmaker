import csv
import random
import time
from multiprocessing import Process

from collector.group_collector import GroupCollector, ProcessResult
from multiprocess_mathmaker.queue_pipe import QueueManagerProxy

MAX_PROCESS_TIME = 1.4


class GroupCollectorProcess(Process):
    def __init__(self, result_queue, queue_connector, rules_collections):
        super().__init__(daemon=True)
        self._result_queue = result_queue
        self._queue_proxy = queue_connector
        self._rules_collections = rules_collections
        self._available_battle_types = list(rules_collections.keys())

    def run(self):
        try:
            while True:
                battle_type = random.choice(self._available_battle_types)
                rules_collection = self._rules_collections[battle_type]
                collector = GroupCollector(self._queue_proxy, battle_type, rules_collection)

                current_time = start_time = time.time()
                result, group = collector.process_battle_groups(current_time)
                process_time = time.time() - start_time
                while result == ProcessResult.NOT_COLLECTED and process_time < MAX_PROCESS_TIME:
                    result, group = collector.process_battle_groups(current_time)
                    process_time = time.time() - start_time
                if result != ProcessResult.COLLECTED:
                    collector.cleanup()

                self._result_queue.put((result, group))
        except Exception as e:
            print(e)
            raise e
