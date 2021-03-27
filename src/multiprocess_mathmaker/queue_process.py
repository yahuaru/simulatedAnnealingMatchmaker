import threading
from multiprocessing import Process, connection, RLock

from matchmaker_queue.queue_manager import QueueManager


class Actions:
    POP = "pop"
    STOP = "stop"


class QueueManagerProcess(Process):
    def __init__(self, queue_key_builders, connectors, enqueue_queue):
        super().__init__(daemon=True)
        self.__queue_manager = QueueManager(queue_key_builders)
        self._connectors = connectors
        self._enqueue_queue = enqueue_queue
        self._active = True

        self._action_to_func = {
            Actions.POP: self._on_pop,
            Actions.STOP: self._on_stop,
        }

        self._lock = RLock()

    def run(self):
        enqueue_thread = threading.Thread(target=self._enqueue, args=())
        enqueue_thread.start()
        connector_thread = threading.Thread(target=self._pipe_recv, args=(self._connectors,))
        connector_thread.start()
        connector_thread.join()
        enqueue_thread.join()

    def _pipe_recv(self, connectors):
        try:
            while self._active:
                ready_connections = connection.wait(connectors)
                for ready_connection in ready_connections:
                    action, args = ready_connection.recv()
                    self._action_to_func[action](ready_connection, args)
        except Exception as e:
            print(e)
            raise e

    def _enqueue(self):
        try:
            while self._active:
                battle_type, division = self._enqueue_queue.get()
                self.__queue_manager.enqueue(battle_type, division)
        except Exception as e:
            print(e)
            raise e

    def _on_stop(self, connector, args):
        self._active = False

    def _on_pop(self, connector, args):
        self._lock.acquire()
        division = self.__queue_manager.pop(*args)
        self._lock.release()
        connector.send(division)

    def _on_enqueue(self, connector, args):
        self._lock.acquire()
        self.__queue_manager.enqueue(*args)
        self._lock.release()