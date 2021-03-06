from abc import ABC, abstractmethod


class IQueueKeyBuilder(ABC):
    @abstractmethod
    def get_division_key(self, division):
        pass

    @abstractmethod
    def get_available_keys(self, battle_group):
        pass
