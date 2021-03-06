from collector.conditions import build_conditions
from collector.rules.base_rules_collection import BaseRulesCollection
from collector.rules.wait_time_rules_collection import WaitTimeRulesCollection
from matchmaker_queue.key import build_queue_key_conditions
from matchmaker_queue.key.key_builder.base_key_builder import BaseQueueKeyBuilder
from matchmaker_queue.key.key_builder.wait_time_queue_key_builder import WaitTimeQueueKeyBuilder


class WaitTimeRulesBuilder:
    @staticmethod
    def build_rules_collection(rules):
        common_conditions = rules['common_conditions']
        rules_by_time = list(rules['by_time'].items())
        rules_by_time.sort(key=lambda item: item[0])
        time_intervals = []
        time_conditions = []
        time_temperatures = []
        time_full_rules = []
        for time, time_rules in rules_by_time:
            full_rules = common_conditions.copy()
            full_rules.update(time_rules)
            time_intervals.append(time)
            time_conditions.append(build_conditions(full_rules))
            time_temperatures.append(full_rules['initial_temperature'])
            time_full_rules.append(full_rules)
        rules_collections = []
        for conditions, temperature, full_rules in zip(time_conditions, time_temperatures, time_full_rules):
            rules_collections.append(BaseRulesCollection(temperature, conditions, full_rules))
        return WaitTimeRulesCollection(time_intervals, rules_collections)

    @staticmethod
    def build_queue_key_builder(rules):
        common_conditions = rules['common_conditions']
        rules_by_time = list(rules['by_time'].items())
        rules_by_time.sort(key=lambda item: item[0])
        time_intervals = []
        time_queue_key_builders = []
        for time, time_rules in rules_by_time:
            full_rules = common_conditions.copy()
            full_rules.update(time_rules)
            time_intervals.append(time)
            conditions = build_queue_key_conditions(full_rules)
            time_queue_key_builders.append(BaseQueueKeyBuilder(conditions))
        return WaitTimeQueueKeyBuilder(time_intervals, time_queue_key_builders)
