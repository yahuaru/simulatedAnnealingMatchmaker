from .key_builder import IQueueKeyBuilder


class BaseQueueKeyBuilder(IQueueKeyBuilder):
    def __init__(self, key_builders):
        self._key_builders = key_builders

    def get_division_key(self, division):
        description_key = []
        for queue_key_builder in self._key_builders:
            description_key.append(queue_key_builder.get_key(division))
        return tuple(description_key)

    def get_available_keys(self, battle_group):
        descriptions = []
        for queue_key_builder in self._key_builders:
            descriptions.append(queue_key_builder.get_available_keys(battle_group))
        return descriptions
