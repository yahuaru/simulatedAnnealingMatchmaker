from abc import ABC, abstractmethod
from typing import Dict, Set, Tuple, List


class IQueueKeyCondition(ABC):
    REQUIRED_FIELDS = set()

    @abstractmethod
    def __init__(self, rules: Dict):
        pass

    @classmethod
    @abstractmethod
    def get_required_rule_fields(cls) -> Set:
        pass

    @abstractmethod
    def get_key(self, division) -> Tuple:
        pass

    @abstractmethod
    def get_available_keys(self, battle_group) -> List:
        pass
