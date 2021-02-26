import random
from typing import Dict, Optional

from matchmaker_queue.key.queue_key_builder import QueueKeyBuilder
from matchmaker_queue.queue import Queue
from battle_group import Division


class QueueManager(object):
    def __init__(self, params: Dict):
        self._params = params

        self._queue_key_builder = QueueKeyBuilder(params)

        self._queues = {}

    def enqueue(self, battle_type, division: Division):
        assert battle_type in self._params, \
            "There no rules for battle type: {} rule: '{}'".format(battle_type, self._params)

        division_key = self._queue_key_builder.get_division_key(battle_type, division)
        battle_type_queues = self._queues.setdefault(battle_type, {})
        queue = battle_type_queues.setdefault(division_key, Queue())
        queue.enqueue(division)

    def dequeue(self, battle_type, division: Division):
        key = self._queue_key_builder.get_division_key(battle_type, division)
        battle_type_queues = self._queues[battle_type]
        if key not in battle_type_queues:
            return
        battle_type_queues[key].dequeue(division)

    def pop(self, battle_type, battle_group, division_size) -> Optional[Division]:
        if battle_type not in self._queues:
            return None

        battle_type_queues = self._queues[battle_type]
        all_division_queues_keys = battle_type_queues.keys()

        available_key_variants = self._queue_key_builder.get_available_keys(battle_type, battle_group)
        division_queues_keys = []
        for queue_key in all_division_queues_keys:
            if all(key_value in available_key_variants[i] for i, key_value in enumerate(queue_key)):
                division_queues_keys.append(queue_key)
        random.shuffle(division_queues_keys)

        for queue_key in division_queues_keys:
            queue = battle_type_queues[queue_key]
            if not queue.is_empty():
                return queue.pop(division_size)

        return None
