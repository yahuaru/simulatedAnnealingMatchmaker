import random

from collector.actions.action import ActionBase
from battle_group import BattleGroup


class SwapDivisionsFromQueueAction(ActionBase):
    def __init__(self, params):
        super().__init__(params)
        self.__max_team_size = params['max_team_size']
        self.__added_division = None
        self.__removed_division = None

    def execute(self, queue, group_key, battle_group):
        if not queue:
            return None

        not_empty_team = [(team_id, team) for team_id, team in enumerate(battle_group.teams) if team.size > 0]
        if not not_empty_team:
            return None

        team_id, team = random.choice(not_empty_team)
        division = random.choice(team.divisions)
        new_battle_group = BattleGroup.remove_division(battle_group, team_id, division)

        free_space = self.__max_team_size - team.size
        division_from_queue = queue.pop(group_key, new_battle_group, division.size + free_space)
        if division_from_queue is None:
            return None

        new_battle_group = BattleGroup.swap_division(battle_group, team_id, division, division_from_queue)

        self.__removed_division = division
        self.__added_division = division_from_queue

        return new_battle_group

    def on_approved(self, queue, battle_type):
        queue.enqueue(battle_type, self.__removed_division)
        self.__added_division = None
        self.__removed_division = None

    def on_rejected(self, queue, battle_type):
        queue.enqueue(battle_type, self.__added_division)
        self.__added_division = None
        self.__removed_division = None
