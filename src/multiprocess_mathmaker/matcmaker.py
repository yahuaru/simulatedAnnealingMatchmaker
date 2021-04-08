import multiprocessing as mp
import time
from threading import Thread

from collector.group_collector import GroupCollector, ProcessResult
from matchmaker_queue.queue_manager import QueueManager
from multiprocess_mathmaker.group_collector_process import GroupCollectorProcess, MAX_PROCESS_TIME
from rules_builder.rules_director import RulesDirector


def process_divisions(queue_builder, rules_collection, divisions):
    results = []
    collected_groups = 0

    queue_manager = QueueManager(queue_builder)

    for division in divisions:
        queue_manager.enqueue(division)

    while collected_groups < 400:
        current_time = start_time = time.time()
        collector = GroupCollector(queue_manager, rules_collection)

        result, group = collector.process_battle_groups(current_time)
        process_time = time.time() - start_time
        while result == ProcessResult.NOT_COLLECTED and process_time < MAX_PROCESS_TIME:
            result, group = collector.process_battle_groups(current_time)
            process_time = time.time() - start_time
        if result != ProcessResult.COLLECTED:
            collector.cleanup()
        else:
            collected_groups += 1
        results.append((start_time, process_time, result))
    return results


class MatchmakerProcessManager:
    def __init__(self, processes_num, rules):
        self._processes_num = processes_num
        self._rules_collections = {}
        self._enqueue_queues = {}
        for battle_type, rules_battle_type in rules.items():
            collection_rules = RulesDirector.build_rules_collector(rules_battle_type)
            queue_rules = RulesDirector.build_queue_key_builder(rules_battle_type)
            self._rules_collections[battle_type] = (collection_rules, queue_rules)
            self._enqueue_queues[battle_type] = []

    def enqueue_division(self, battle_type, division):
        self._enqueue_queues[battle_type].append(division)

    def start_process(self):
        args = []
        for i, (battle_type, (collection_rules, queue_rules)) in enumerate(self._rules_collections.items()):
            args.append((queue_rules, collection_rules, self._enqueue_queues[battle_type]))

        with mp.Pool(self._processes_num) as p:
            result = p.starmap(process_divisions, args)

        return result

