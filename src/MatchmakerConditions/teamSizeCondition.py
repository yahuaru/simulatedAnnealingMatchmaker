from MatchmakerConditions.condition import Condition


class TeamSizeCondition(Condition):
    def __init__(self, params):
        super().__init__(params)
        self.__team_size = params['team_size']

    def check(self, battle_group):
        penalty = 0
        for i, team in enumerate(battle_group.teams[:-1]):
            penalty += (self.__team_size - team.size)
        return penalty
