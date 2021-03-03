from typing import Set
from .condition import ICondition


class TeamSizeCondition(ICondition):
    def __init__(self, rules):
        super().__init__(rules)
        self.__min_team_size = rules['min_team_size']
        self.__max_team_size = rules['max_team_size']

        self.__team_size_equal = rules.get('team_size_equal', True)

    @classmethod
    def get_required_rule_fields(cls) -> Set:
        return {'min_team_size', 'max_team_size'}

    def check(self, battle_group):
        max_team_size = max(team.size for team in battle_group.teams)

        penalty = 0
        for team in battle_group.teams:
            if max_team_size >= self.__min_team_size and self.__team_size_equal:
                penalty += abs(max_team_size - team.size)
            else:
                penalty += max((self.__min_team_size - team.size), 0)
        return penalty
