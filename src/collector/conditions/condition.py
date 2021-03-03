from abc import ABC, abstractmethod


class ICondition(ABC):
    ACTIONS = set()
    REQUIRED_RULE_FIELDS = set()

    @abstractmethod
    def __init__(self, params):
        pass

    @abstractmethod
    def check(self, battle_group):
        return 0
