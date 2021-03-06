from abc import ABC, abstractmethod
from collections import namedtuple


RulesState = namedtuple("RulesState", ["temperature", "penalty", "rules"])


class IRulesCollection(ABC):
    @abstractmethod
    def get_state(self, battle_group) -> RulesState:
        pass
