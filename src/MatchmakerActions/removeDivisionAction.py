import random

from MatchmakerActions.action import SimulatedAnnealingAction
from battleGroup import BattleGroup


class RemoveDivisionAction(SimulatedAnnealingAction):
    def __init__(self, params):
        super().__init__(params)
        self.__removed_division = None

    def execute(self, queue, battle_group):
        not_empty_team = [(team_id, team) for team_id, team in enumerate(battle_group.teams) if team.size > 0]
        if not not_empty_team:
            return None

        team_id, team = random.choice(not_empty_team)
        division = random.choice(team.divisions)

        new_battle_group = BattleGroup.removeDivision(battle_group, team_id, division)

        self.__removed_division = division
        return new_battle_group

    def on_approved(self, queue):
        queue.enqueue(self.__removed_division)
        self.__removed_division = None

    def on_rejected(self, queue):
        self.__removed_division = None
