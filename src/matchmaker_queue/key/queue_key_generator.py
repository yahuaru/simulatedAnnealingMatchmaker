from abc import ABC, abstractmethod
from typing import Dict


class IQueueKeyGenerator(ABC):
    REQUIRED_FIELDS = set()

    @abstractmethod
    def __init__(self, params: Dict):
        pass

    @abstractmethod
    def get_key(self, division):
        pass

    @abstractmethod
    def get_group_keys(self, division):
        pass
