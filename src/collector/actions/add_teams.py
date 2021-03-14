from battle_group.battle_group import BattleGroup
from .action import ActionBase


class AddTeamsAction(ActionBase):
    def __init__(self, rules):
        super().__init__(rules)
        self.__teams_num = rules['teams_num']

    def execute(self, current_time, queue, battle_type, battle_group: BattleGroup):
        if battle_group.size() >= self.__teams_num:
            return None
        return battle_group.extend_size(current_time, self.__teams_num)
