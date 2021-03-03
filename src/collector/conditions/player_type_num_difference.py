from typing import Set

from .condition import ICondition
from player import PlayerType


class PlayerTypeNumDifferenceCondition(ICondition):
    def __init__(self, params):
        super().__init__(params)
        self.__player_type_num_diff = params['player_type_num_diff']
        self.__teams_num = params['teams_num']

    @classmethod
    def get_required_rule_fields(cls) -> Set:
        return {"player_type_num_diff", "teams_num"}

    def check(self, battle_group):
        penalty = 0
        player_types = list(PlayerType)
        player_types_num = len(player_types)

        for i, team in enumerate(battle_group.teams[:-1]):
            if team.size > 0:
                for otherTeam in battle_group.teams[i + 1:]:
                    for playerType in player_types:
                        type_num = team.players_types_num[playerType]
                        other_type_num = otherTeam.players_types_num[playerType]
                        delta_ship_type = abs(type_num - other_type_num)
                        if delta_ship_type > self.__player_type_num_diff[playerType]:
                            penalty += 1
            else:
                penalty += (self.__teams_num - i - 1) * player_types_num

        return penalty
