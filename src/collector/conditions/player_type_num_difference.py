from typing import Set

from .condition import ICondition
from player import PlayerType


class PlayerTypeNumDifferenceCondition(ICondition):
    def __init__(self, rules):
        super().__init__(rules)
        self.__player_type_num_diff = rules['player_type_num_diff']
        self.__teams_num = rules['teams_num']

    @classmethod
    def get_required_rule_fields(cls) -> Set:
        return {"player_type_num_diff", "teams_num"}

    def check(self, battle_group):
        penalty_per_team = sum(self.__player_type_num_diff.values())
        if battle_group.is_empty():
            penalty_per_team = len(self.__player_type_num_diff)
            return self.__teams_num * (self.__teams_num - 1) / 2 * penalty_per_team

        penalty = 0
        for i, team in enumerate(battle_group.teams[:-1]):
            if team.size > 0:
                for otherTeam in battle_group.teams[i + 1:]:
                    for playerType in PlayerType:
                        type_num = team.players_types_num[playerType]
                        other_type_num = otherTeam.players_types_num[playerType]
                        delta_ship_type = abs(type_num - other_type_num)
                        player_type_num_diff = self.__player_type_num_diff[playerType]
                        if delta_ship_type > player_type_num_diff:
                            penalty += delta_ship_type - player_type_num_diff
            else:
                penalty += (self.__teams_num - i - 1) * penalty_per_team

        return penalty
