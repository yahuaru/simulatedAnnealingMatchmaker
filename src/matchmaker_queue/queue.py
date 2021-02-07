import heapq
import random
from collections import namedtuple

QueueEntry = namedtuple("SimulatedAnnealingMatchmakerQueueEntry", ["priority", "id"])

STIR_COEFFICIENT = 5


class Queue(object):
    def __init__(self):
        self._divisions = {}
        self._queue_by_size = {}

    def enqueue(self, division):
        priority = division.enqueue_time + STIR_COEFFICIENT * random.random()
        entry = QueueEntry(priority, division.id)
        queue = self._queue_by_size.setdefault(division.size, [])
        heapq.heappush(queue, entry)
        self._divisions[division.id] = division

    def dequeue(self, division):
        del self._divisions[division.id]

    def pop(self, size):
        if not self._queue_by_size:
            return None

        fit_key_sizes = []
        for key_size in self._queue_by_size:
            if key_size <= size:
                fit_key_sizes.append(key_size)

        random.shuffle(fit_key_sizes)
        for key_size in fit_key_sizes:
            division = None
            queue = self._queue_by_size[key_size]
            while queue and division is None:
                division_id = heapq.heappop(queue)
                division = self._divisions.pop(division_id, None)
            if not queue:
                del self._queue_by_size[key_size]
            if division is not None:
                return division
        return None

    def clear(self):
        self._queue_by_size.clear()

    def __iter__(self):
        return iter(self._queue_by_size)


