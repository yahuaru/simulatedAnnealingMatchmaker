import bisect
import heapq
import math
import random
from collections import namedtuple

QueueEntry = namedtuple("SimulatedAnnealingMatchmakerQueueEntry", ["priority", "division_id", "division"])

POP_PRIORITY_COEFFICIENT = 0.2


class Queue(object):
    def __init__(self):
        self._divisions = {}
        self._queue_by_size = {}

    def is_empty(self):
        return len(self._queue_by_size) == 0

    def enqueue(self, division):
        assert division.id not in self._divisions
        # stir little bit, so division didn't place with the same divisions again
        entry = QueueEntry(division.enqueue_time, division.id, division)
        queue = self._queue_by_size.setdefault(division.size, [])
        bisect.insort(queue, entry)

    def dequeue(self, division):
        self._queue_by_size[division.size].remove(division)

    def pop(self, size):
        if not self._queue_by_size:
            return None

        # select queues with fit division sizes and pop division from selected random queue
        fit_key_sizes = []
        for key_size in self._queue_by_size:
            if key_size <= size:
                fit_key_sizes.append(key_size)
        random.shuffle(fit_key_sizes)

        for key_size in fit_key_sizes:
            queue = self._queue_by_size[key_size]
            entry = queue.pop(random.randint(0, int(len(queue) * POP_PRIORITY_COEFFICIENT)))
            if not queue:
                del self._queue_by_size[key_size]
            return entry.division

        return None

    def clear(self):
        self._queue_by_size.clear()

    def __iter__(self):
        return iter(self._queue_by_size)


