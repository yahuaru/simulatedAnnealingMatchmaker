from abc import ABC, abstractmethod

from battleGroup import BattleGroup
from matchmaker_queue.key.queue_key_builder import QueueGroupKey


class ActionBase(ABC):
    def __init__(self, params):
        pass

    @abstractmethod
    def execute(self, queue, group_key: QueueGroupKey, battle_group: BattleGroup):
        pass

    def on_approved(self, queue, group_key: QueueGroupKey):
        pass

    def on_rejected(self, queue, group_key: QueueGroupKey):
        pass
