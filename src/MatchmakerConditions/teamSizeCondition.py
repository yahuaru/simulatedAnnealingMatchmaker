import math

from MatchmakerActions.addDivisionAction import AddDivisionAction
from MatchmakerActions.removeDivisionAction import RemoveDivisionAction
from MatchmakerActions.swapDivisionFromQueueAction import SwapDivisionsFromQueueAction
from MatchmakerActions.swapDivisionsAction import SwapDivisionsAction
from MatchmakerConditions.condition import Condition


class TeamSizeCondition(Condition):
    ACTIONS = {AddDivisionAction, SwapDivisionsAction, RemoveDivisionAction, SwapDivisionsFromQueueAction}
    REQUIRED_PARAMS = {'teams_num', 'min_team_size', 'max_team_size'}

    def __init__(self, params):
        super().__init__(params)
        self.__min_team_size = params['min_team_size']
        self.__max_team_size = params['max_team_size']

        self.__team_size_equal = params.get('team_size_equal', True)

    def check(self, battle_group):
        max_team_size = max(team.size for team in battle_group.teams)

        penalty = 0
        for team in battle_group.teams:
            if max_team_size >= self.__min_team_size and self.__team_size_equal:
                penalty += abs(max_team_size - team.size)
            else:
                penalty += max((self.__min_team_size - team.size), 0)
        return penalty
