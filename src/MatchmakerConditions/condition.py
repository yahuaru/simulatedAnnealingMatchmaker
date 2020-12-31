from abc import ABC


class Condition(ABC):
    ACTIONS = ()

    def __init__(self, params):
        pass

    def check(self, battle_group):
        return 0