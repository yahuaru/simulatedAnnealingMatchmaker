from multiprocessing import connection

from battle_group.division import Division
from multiprocess_mathmaker.queue_process import Actions


class QueueManagerProxy:
    def __init__(self, queue, connector: connection.Connection):
        self._queue = queue
        self._connector = connector

    def pop(self, battle_type, battle_group, division_size) -> Division:
        self._connector.send((Actions.POP, (battle_type, battle_group, division_size)))
        return self._connector.recv()

    def enqueue(self, battle_type, division):
        self._queue.put((battle_type, division))
