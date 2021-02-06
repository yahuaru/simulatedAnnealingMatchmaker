import bisect
import random
from collections import namedtuple
from threading import RLock, Semaphore

QueueEntry = namedtuple("SimulatedAnnealingMatchmakerQueueEntry", ["enqueue_time", "id", "division"])


def _threadOperation(func):
    def wrapper(self, *args, **kwargs):
        self._lock.acquire()
        result = func(self, *args, **kwargs)
        self._lock.release()
        return result
    return wrapper

#
# class SimulatedAnnealingMatchmakerQueue:
#     def __init__(self, queue=None):
#         self._lock = Semaphore()
#
#         self.__queue = []
#         if queue is not None:
#             self.__queue = sorted([QueueEntry(division.enqueue_time, division.id, division) for division in queue])
#
#     def pushDivision(self, division):
#         entry = QueueEntry(division.enqueue_time, division.id, division)
#         bisect.insort(self.__queue, entry)
#
#     def removeDivision(self, division):
#         entry = QueueEntry(division.enqueue_time, division.id, division)
#         self.__queue.remove(entry)
#
#     def popDivisionBySize(self, size):
#         if not self.__queue:
#             return None
#
#         random_start_pos = int(pow(0.2, 8*random.random()) * len(self.__queue))
#
#         index = -1
#         for i, entry in enumerate(self.__queue[random_start_pos:], random_start_pos):
#             if entry.division.size <= size:
#                 index = i
#                 break
#         if index == -1:
#             return None
#
#         return self.__queue.pop(index).division
#
#     def clear(self):
#         self.__queue.clear()
#
#     def __len__(self):
#         return len(self.__queue)
#
#     def __iter__(self):
#         return iter(self.__queue)

