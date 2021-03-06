import random

from collector.actions.action import ActionBase
from battle_group import BattleGroup


class AddDivisionAction(ActionBase):
    def __init__(self, params):
        super().__init__(params)
        self.__max_team_size = params['max_team_size']
        self.__added_division = None

    def execute(self, queue, group_key, battle_group):
        if not queue:
            return None

        vacant_teams = [(i, team) for i, team in enumerate(battle_group.teams) if team.size < self.__max_team_size]
        if not vacant_teams:
            return None

        team_id, vacant_team = random.choice(vacant_teams)
        division_from_queue = queue.pop(group_key, battle_group, self.__max_team_size - vacant_team.size)
        if division_from_queue is None:
            return None

        new_battle_group = BattleGroup.add_division(battle_group, team_id, division_from_queue)
        self.__added_division = division_from_queue

        return new_battle_group

    def on_approved(self, queue, battle_type):
        self.__added_division = None

    def on_rejected(self, queue, battle_type):
        queue.enqueue(battle_type, self.__added_division)
        self.__added_division = None

