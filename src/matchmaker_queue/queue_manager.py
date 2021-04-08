import random
from typing import Optional

from matchmaker_queue.queue import Queue
from battle_group.division import Division


class QueueManager:
    def __init__(self, queue_key_builders):
        self._queue_key_builders = queue_key_builders
        self._queues = {}

    def enqueue(self, division: Division):
        division_key = self._queue_key_builders.get_division_key(division)
        queue = self._queues.setdefault(division_key, Queue())
        queue.enqueue(division)

    def dequeue(self, division: Division):
        key = self._queue_key_builders.get_division_key(division)
        battle_type_queues = self._queues
        if key not in battle_type_queues:
            return
        battle_type_queues[key].dequeue(division)

    def pop(self, battle_group, division_size) -> Optional[Division]:
        all_division_queues_keys = self._queues.keys()

        available_key_variants = self._queue_key_builders.get_available_keys(battle_group)
        division_queues_keys = []
        for queue_key in all_division_queues_keys:
            if all(key_value in available_key_variants[i] for i, key_value in enumerate(queue_key)):
                division_queues_keys.append(queue_key)
        random.shuffle(division_queues_keys)

        for queue_key in division_queues_keys:
            queue = self._queues[queue_key]
            if not queue.is_empty():
                return queue.pop(division_size)

        return None

    def __len__(self):
        return sum(len(queue) for queue in self._queues.values())
