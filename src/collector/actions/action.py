from abc import ABC, abstractmethod

from battle_group.battle_group import BattleGroup


class ActionBase(ABC):
    def __init__(self, rules):
        pass

    @abstractmethod
    def execute(self, current_time, queue, battle_group: BattleGroup):
        pass

    def on_approved(self, queue):
        pass

    def on_rejected(self, queue):
        pass
