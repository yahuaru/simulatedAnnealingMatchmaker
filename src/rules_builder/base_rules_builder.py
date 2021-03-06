from collector.conditions import build_conditions
from collector.rules.base_rules_collection import BaseRulesCollection
from matchmaker_queue.key import build_queue_key_conditions
from matchmaker_queue.key.key_builder.base_key_builder import BaseQueueKeyBuilder
from rules_builder.rules_builder import IRulesBuilder


class BaseRulesBuilder(IRulesBuilder):
    @staticmethod
    def build_rules_collection(rules):
        conditions = build_conditions(rules)
        initial_temperature = rules['initial_temperature']
        return BaseRulesCollection(rules, initial_temperature, conditions)

    @staticmethod
    def build_queue_key_builder(rules):
        queue_key_conditions = build_queue_key_conditions(rules)
        return BaseQueueKeyBuilder(queue_key_conditions)
