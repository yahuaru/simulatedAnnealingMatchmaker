from typing import Dict

from rules_builder.base_rules_builder import BaseRulesBuilder
from rules_builder.wait_time_rules_builder import WaitTimeRulesBuilder

TYPE_TO_COLLECTION = {
    'base': BaseRulesBuilder,
    'by_time': WaitTimeRulesBuilder,
}


class RulesDirector:
    @staticmethod
    def build_rules_collector(rules: Dict):
        rules_type = rules['type']
        rules_collection_builder = TYPE_TO_COLLECTION[rules_type]
        return rules_collection_builder.build_rules_collection(rules)

    @staticmethod
    def build_queue_key_builder(rules: Dict):
        rules_type = rules['type']
        queue_key_builder = TYPE_TO_COLLECTION[rules_type]
        return queue_key_builder.build_queue_key_builder(rules)
