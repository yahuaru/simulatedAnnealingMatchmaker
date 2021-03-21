import threading
from multiprocessing import Process

from matchmaker_queue.queue_manager import QueueManager


class Actions:
    POP = "pop"
    ENQUEUE = "enqueue"
    STOP = "stop"


class QueueManagerProcess(Process):
    def __init__(self, queue_key_builders, connectors):
        super().__init__(daemon=True)
        self.__queue_manager = QueueManager(queue_key_builders)
        self._connectors = connectors
        self._active = True

        self._action_to_func = {
            Actions.POP: self._on_pop,
            Actions.ENQUEUE: self._on_enqueue,
            Actions.STOP: self._on_stop,
        }

    def run(self):
        connectors_threads = []
        for connector in self._connectors:
            connector_thread = threading.Thread(target=self._pipe_recv, args=(connector,))
            connectors_threads.append(connector_thread)
            connector_thread.start()
        for connector_thread in connectors_threads:
            connector_thread.join()

    def _pipe_recv(self, connector):
        try:
            while self._active:
                action, args = connector.recv()
                self._action_to_func[action](connector, args)
        except Exception as e:
            print(e)
            raise e

    def _on_stop(self, connector, args):
        self._active = False

    def _on_pop(self, connector, args):
        division = self.__queue_manager.pop(*args)
        connector.send(division)

    def _on_enqueue(self, connector, args):
        self.__queue_manager.enqueue(*args)