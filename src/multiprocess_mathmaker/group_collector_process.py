import time
from multiprocessing import Process

from collector.group_collector import GroupCollector, ProcessResult
from matchmaker_queue.queue_manager import QueueManager

MAX_PROCESS_TIME = 0.7


class GroupCollectorProcess(Process):
    def __init__(self, name, result_queue, rules_collection, queue_builder, divisions):
        super().__init__(daemon=True, name=name)
        self._result_queue = result_queue
        self._queue_manager = QueueManager(queue_builder)
        self._rules_collection = rules_collection
        self._enqueue_queue = divisions

    def run(self):
        super().run()
        collected_groups = 0
        try:
            for division in self._enqueue_queue:
                self._queue_manager.enqueue(division)

            while collected_groups < 400:
                current_time = start_time = time.time()
                collector = GroupCollector(self._queue_manager, self._rules_collection)

                result, group = collector.process_battle_groups(current_time)
                process_time = time.time() - start_time
                while result == ProcessResult.NOT_COLLECTED and process_time < MAX_PROCESS_TIME:
                    result, group = collector.process_battle_groups(current_time)
                    process_time = time.time() - start_time
                if result != ProcessResult.COLLECTED:
                    collector.cleanup()
                else:
                    collected_groups += 1

                self._result_queue.put((self.name, start_time, process_time, result, group))

        except Exception as e:
            print(e)
            raise e
