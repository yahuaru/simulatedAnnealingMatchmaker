from abc import ABC


class Condition(ABC):
    ACTIONS = set()
    REQUIRED_PARAMS = set()

    def __init__(self, params):
        pass

    def check(self, battle_group):
        return 0
