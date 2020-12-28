from MatchmakerConditions.Condition import Condition
from player import PlayerType


class PlayerTypeNumDifferenceCondition(Condition):
    def __init__(self, params):
        super().__init__(params)
        self.__player_type_num_diff = params['player_type_num_diff']
        self.__teams_num = params['teams_num']

    def check(self, battle_group):
        energy = 0
        for i, team in enumerate(battle_group.teams[:-1]):
            if team.size > 0:
                for otherTeam in battle_group.teams[i + 1:]:
                    for playerType in list(PlayerType):
                        type_num = team.playersTypesNum[playerType]
                        other_type_num = otherTeam.playersTypesNum[playerType]
                        delta_ship_type = abs(type_num - other_type_num)
                        if delta_ship_type > self.__player_type_num_diff[playerType]:
                            energy += 1
                            break

            else:
                energy += (self.__teams_num - i - 1)

        return energy