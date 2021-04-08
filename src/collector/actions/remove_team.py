from random import randint

from battle_group.battle_group import BattleGroup
from .action import ActionBase


class RemoveTeamAction(ActionBase):
    def __init__(self, rules):
        super().__init__(rules)
        self.__teams_num = rules['teams_num']

    def execute(self, current_time, queue, battle_group: BattleGroup):
        if battle_group.size() <= self.__teams_num:
            return None

        for team_id, team in enumerate(battle_group):
            if team.size == 0:
                return battle_group.remove_team(current_time, team_id)

        return battle_group.remove_team(current_time, randint(0, battle_group.size() - 1))
