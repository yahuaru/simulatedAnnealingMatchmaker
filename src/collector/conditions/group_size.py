from typing import Set
from .condition import ICondition


class GroupSizeCondition(ICondition):
    def __init__(self, rules):
        super().__init__(rules)
        self.__teams_num = rules['teams_num']

    @classmethod
    def get_required_rule_fields(cls) -> Set:
        return {'teams_num', }

    def check(self, battle_group):
        return abs(battle_group.size() - self.__teams_num)
