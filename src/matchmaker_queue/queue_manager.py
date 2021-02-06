import random
from typing import Dict, Optional

from matchmaker_queue.key.queue_key_builder import QueueKeyBuilder, QueueGroupKey
from matchmaker_queue.queue import Queue
from battleGroup import Division


class QueueManager(object):
    def __init__(self, params: Dict):
        self._params = params

        self._queue_key_builder = QueueKeyBuilder(params)

        self._queues = {}
        self._groups_queues = {}

        self._available_group_keys = []

    def enqueue(self, battle_type, division: Division):
        assert battle_type in self._params, \
            "There no rules for battle type: {} rule: '{}'".format(battle_type, self._params)

        division_key = self._queue_key_builder.get_division_key(battle_type, division)
        if division_key not in self._queues:
            queue = Queue()
            self._queues[division_key] = queue
            group_keys = self._queue_key_builder.get_group_keys(battle_type, division)
            for key in group_keys:
                if key not in self._groups_queues:
                    self._groups_queues[key] = {}
                    self._available_group_keys.append(key)
                self._groups_queues[key][division_key] = queue
        else:
            queue = self._queues[division_key]
        queue.enqueue(division)

    def dequeue(self, battle_type, division: Division):
        keys = self._queue_key_builder.get_group_keys(battle_type, division)
        for key in keys:
            if key not in self._queues:
                return
            self._queues[key].dequeue(division)

    def pop(self, group_key, division_size) -> Optional[Division]:
        group_queues = list(self._groups_queues[group_key].values())
        random.shuffle(group_queues)
        for queue in group_queues:
            if queue:
                return queue.pop(division_size)
        return None

    def push_key(self, key):
        assert key in self._groups_queues, "Group key:{} not in queues:{}".format(key, self._groups_queues.keys())
        self._available_group_keys.append(key)

    def get_next_available_group_key(self) -> Optional[QueueGroupKey]:
        if not self._available_group_keys:
            return None
        return self._available_group_keys.pop(0)


