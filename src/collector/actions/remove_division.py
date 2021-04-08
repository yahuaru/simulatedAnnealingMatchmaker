import random

from collector.actions.action import ActionBase
from battle_group.battle_group import BattleGroup


class RemoveDivisionAction(ActionBase):
    def __init__(self, params):
        super().__init__(params)
        self.__removed_division = None

    def execute(self, current_time, queue, battle_group):
        if battle_group.is_empty():
            return None

        not_empty_team = [(team_id, team) for team_id, team in enumerate(battle_group.teams) if team.size > 0]
        if not not_empty_team:
            return None

        team_id, team = random.choice(not_empty_team)
        division = random.choice(team.divisions)

        new_battle_group = battle_group.remove_division(current_time, team_id, division)

        self.__removed_division = division
        return new_battle_group

    def on_approved(self, queue):
        queue.enqueue(self.__removed_division)
        self.__removed_division = None

    def on_rejected(self, queue):
        self.__removed_division = None
