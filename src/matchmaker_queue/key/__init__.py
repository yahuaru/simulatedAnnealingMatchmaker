from typing import List

from .queue_key_by_level import ByLevelQueueKeyCondition

QUEUE_KEY_BUILDERS = (ByLevelQueueKeyCondition,)


def build_queue_key_conditions(rules) -> List:
    rules_keys = set(rules.keys())
    key_builders = []
    for queue_key_builder in QUEUE_KEY_BUILDERS:
        if queue_key_builder.get_required_rule_fields().issubset(rules_keys):
            key_builders.append(queue_key_builder(rules_keys))
    return key_builders
