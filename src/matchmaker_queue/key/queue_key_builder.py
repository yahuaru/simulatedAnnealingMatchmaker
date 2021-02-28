from matchmaker_queue.key.queue_key_by_level import QueueKeyByLevel


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

    def get_division_key(self, battle_type, division):
        description_key = []
        for queue_key_builder in self._queue_key_builders[battle_type]:
            description_key.append(queue_key_builder.get_key(division))
        return tuple(description_key)

    def get_available_keys(self, battle_type, battle_group):
        descriptions = []
        for queue_key_builder in self._queue_key_builders[battle_type]:
            descriptions.append(queue_key_builder.get_available_keys(battle_group))
        return descriptions
