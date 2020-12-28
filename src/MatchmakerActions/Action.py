from abc import ABC


class SimulatedAnnealingAction(ABC):
    def __init__(self, params):
        pass

    def execute(self, queue, battle_group):
        pass

    def on_approved(self, queue):
        pass

    def on_rejected(self, queue):
        pass