from abc import ABC, abstractmethod
from typing import Set


class ICondition(ABC):
    @abstractmethod
    def __init__(self, rules):
        pass

    @classmethod
    @abstractmethod
    def get_required_rule_fields(cls) -> Set:
        return set()

    @abstractmethod
    def check(self, battle_group) -> int:
        return 0
