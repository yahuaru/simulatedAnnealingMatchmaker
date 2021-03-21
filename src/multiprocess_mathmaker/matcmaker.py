import multiprocessing as mp
from threading import Thread

from multiprocess_mathmaker.group_collector_process import GroupCollectorProcess
from multiprocess_mathmaker.queue_pipe import QueueManagerProxy
from multiprocess_mathmaker.queue_process import QueueManagerProcess
from rules_builder.rules_director import RulesDirector


class MatchmakerProcessManager:
    def __init__(self, process_num, rules):

        self._process_num = process_num
        self._collector_processes = []
        self.__available_battle_types = []
        self._rules_collections = {}
        self._queue_key_builders = {}
        for battle_type, rules_battle_type in rules.items():
            self.__available_battle_types.append(battle_type)
            self._rules_collections[battle_type] = RulesDirector.build_rules_collector(rules_battle_type)
            self._queue_key_builders[battle_type] = RulesDirector.build_queue_key_builder(rules_battle_type)

        self._queue_connectors = []
        self._collector_connectors = []
        self._queue_connector = None
        self._queue_process = None

        self._result_queue = None
        self._result_collection_thread = None

    def enqueue_division(self, battle_type, division):
        self._queue_connector.enqueue(battle_type, division)

    def start_process(self):
        mp.set_start_method('spawn')
        self._result_queue = mp.Queue()

        queue_connector, matchmaker_connector = mp.Pipe()
        self._queue_connectors.append(queue_connector)
        self._queue_connector = QueueManagerProxy(matchmaker_connector)

        for i in range(self._process_num):
            queue_connector, collector_connector = mp.Pipe()
            self._queue_connectors.append(queue_connector)
            self._collector_connectors.append(collector_connector)
            process = GroupCollectorProcess(self._result_queue, self._collector_connectors[i], self._rules_collections)
            self._collector_processes.append(process)

        self._queue_process = QueueManagerProcess(self._queue_key_builders, self._queue_connectors)
        self._queue_process.start()

        self._result_collection_thread = Thread(target=self._collect_result)
        self._result_collection_thread.start()

        for process in self._collector_processes:
            process.start()

    def _collect_result(self):
        while True:
            result = self._result_queue.get()
            print(result)

    # def dequeue_division(self, battle_type, division):
    #     self.queue_connector.dequeue(battle_type, division)
