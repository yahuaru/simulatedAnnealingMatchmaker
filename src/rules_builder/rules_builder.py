from abc import abstractmethod, ABC

from collector.rules.rules_collection import IRulesCollection
from matchmaker_queue.key.key_builder.key_builder import IQueueKeyBuilder


class IRulesBuilder(ABC):
    @staticmethod
    @abstractmethod
    def build_rules_collection(rules) -> IRulesCollection:
        pass

    @staticmethod
    @abstractmethod
    def build_queue_key_builder(rules) -> IQueueKeyBuilder:
        pass
