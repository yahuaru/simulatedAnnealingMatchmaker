from collections import namedtuple

QueueEntry = namedtuple("SimulatedAnnealingMatchmakerQueueEntry", ["enqueue_time", "id", "division"])


class SimulatedAnnealingMatchmakerQueue:
    def __init__(self, queue=None):
        self.__queue = []
        if queue is not None:
            self.__queue = sorted([QueueEntry(division.enqueue_time, division.id, division) for division in queue])

    def pushDivision(self, division):
        entry = QueueEntry(division.enqueue_time, division.id, division)
        self.__queue.append(entry)

    def removeDivision(self, division):
        entry = QueueEntry(division.enqueue_time, division.id, division)
        self.__queue.remove(entry)

    def removeByIndex(self, index):
        del self.__queue[index]

    def clear(self):
        self.__queue.clear()

    def __len__(self):
        return len(self.__queue)

    def __iter__(self):
        return iter(self.__queue)

