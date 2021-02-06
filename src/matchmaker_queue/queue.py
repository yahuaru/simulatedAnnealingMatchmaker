import bisect
import random
from collections import namedtuple

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


