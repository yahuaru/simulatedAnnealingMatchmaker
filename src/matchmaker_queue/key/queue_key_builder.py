from collections import namedtuple
from typing import List, Tuple

from matchmaker_queue.key.queue_key_by_level import QueueKeyByLevel

QueueGroupKey = namedtuple("QueueGroupKey", ["battle_type", "description"])


class QueueKeyBuilder(object):
    QUEUE_KEY_BUILDERS = (QueueKeyByLevel,)

    def __init__(self, params):
        self._queue_key_builders = {}
        for battle_type, battle_param in params.items():
            self._queue_key_builders[battle_type] = []

            common_params = battle_param['common_conditions']
            param_keys = set(common_params.keys())
            param_by_time = battle_param['by_time']
            param_keys = param_keys | set(key for param in param_by_time.values() for key in param.keys())
            for queue_key_builder in QueueKeyBuilder.QUEUE_KEY_BUILDERS:
                if queue_key_builder.REQUIRED_FIELDS.issubset(param_keys):
                    self._queue_key_builders[battle_type].append(queue_key_builder(battle_param))

    def get_division_key(self, battle_type, division) -> Tuple:
        description_key = []
        for queue_key_builder in self._queue_key_builders[battle_type]:
            description_key.append(queue_key_builder.get_key(division))
        return tuple(description_key)

    def get_group_keys(self, battle_type, division) -> List[QueueGroupKey]:
        descriptions = [()]
        for queue_key_builder in self._queue_key_builders[battle_type]:
            new_descriptions = []
            for description in descriptions:
                for key_entry in queue_key_builder.get_group_keys(division):
                    new_descriptions.append(description + (key_entry,))
            descriptions = new_descriptions
        return [QueueGroupKey(battle_type, description) for description in descriptions]