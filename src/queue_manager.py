import bisect
import random
from collections import namedtuple
from typing import Dict, Optional, Tuple, List

from battleGroup import Division


class QueueKeyByLevel:
    REQUIRED_FIELDS = {"by_level", }

    def __init__(self, params: Dict):
        by_level_rules = params['common_conditions']['by_level']
        self._max_level_difference = by_level_rules['max_level_difference']
        self._min_level = by_level_rules['min_level']
        self._max_level = by_level_rules['max_level']

    def get_keys(self, division) -> List:
        min_level_key = max(division.max_level, self._min_level + self._max_level_difference)
        max_level_key = min(division.max_level + self._max_level_difference,
                            self._max_level - self._max_level_difference)
        return [i for i in range(min_level_key, max_level_key + 1)]


class QueueKeyBuilder(object):
    QUEUE_KEY_BUILDERS = (QueueKeyByLevel,)

    def __init__(self, params):
        self._queue_key_builders = {}
        for battle_type, battle_param in params.items():
            self._queue_key_builders[battle_type] = []

            common_params = battle_param['common_conditions']
            param_keys = set(common_params.keys())
            param_by_time = battle_param['by_time']
            param_keys = param_keys | set(key for param in param_by_time.values() for key in param.keys())
            for queue_key_builder in QueueKeyBuilder.QUEUE_KEY_BUILDERS:
                if queue_key_builder.REQUIRED_FIELDS.issubset(param_keys):
                    self._queue_key_builders[battle_type].append(queue_key_builder(battle_param))

    def get_keys(self, battle_type, division) -> List[Tuple]:
        keys = [(battle_type,)]
        for queue_key_builder in self._queue_key_builders[battle_type]:
            new_keys = []
            for key in keys:
                for key_entry in queue_key_builder.get_keys(division):
                    new_keys.append(key + (key_entry,))
            keys = new_keys
        return keys


QueueEntry = namedtuple("SimulatedAnnealingMatchmakerQueueEntry", ["enqueue_time", "id", "division"])


class Queue(object):
    def __init__(self):
        self._queue = []

    def __len__(self):
        return len(self._queue)

    def enqueue(self, division):
        entry = QueueEntry(division.enqueue_time, division.id, division)
        bisect.insort(self._queue, entry)

    def dequeue(self, division):
        entry = QueueEntry(division.enqueue_time, division.id, division)
        self._queue.remove(entry)

    def pop(self, size):
        if not self._queue:
            return None

        random_start_pos = int(pow(0.2, 8*random.random()) * len(self._queue))

        index = -1
        for i, entry in enumerate(self._queue[random_start_pos:], random_start_pos):
            if entry.division.size <= size:
                index = i
                break
        if index == -1:
            return None

        return self._queue.pop(index).division

    def clear(self):
        self._queue.clear()

    def __iter__(self):
        return iter(self._queue)



QueueManagerEntry = namedtuple("QueueManagerEntry", ["key", "battle_type", "queue"])


class QueueManager(object):
    def __init__(self, params: Dict):
        self._params = params

        self._queue_key_builder = QueueKeyBuilder(params)

        self._queues = {}
        self._available_queues = []

    def enqueue(self, battle_type, division: Division):
        assert battle_type in self._params, \
            "There no rules for battle type: {} rule: '{}'".format(battle_type, self._params)

        keys = self._queue_key_builder.get_keys(battle_type, division)
        for key in keys:
            if key not in self._queues:
                queue = Queue()
                self._queues[key] = queue
                entry = QueueManagerEntry(key, battle_type, queue)
                self._available_queues.append(entry)

            self._queues[key].enqueue(division)

    def dequeue(self, battle_type, division: Division):
        keys = self._queue_key_builder.get_keys(battle_type, division)
        for key in keys:
            if key not in self._queues:
                return
            self._queues[key].dequeue(division)

    def get_next_available_queue(self) -> Optional[QueueManagerEntry]:
        while self._available_queues:
            entry = self._available_queues.pop(0)
            if entry.queue:
                return entry
        return None
