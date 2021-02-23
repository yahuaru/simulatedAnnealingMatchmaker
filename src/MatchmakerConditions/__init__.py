from MatchmakerConditions.level_difference_condition import LevelDifferenceCondition
from MatchmakerConditions.player_type_num_difference import PlayerTypeNumDifferenceCondition
from MatchmakerConditions.team_size_condition import TeamSizeCondition

CONDITIONS = (TeamSizeCondition, PlayerTypeNumDifferenceCondition, LevelDifferenceCondition)


def buildConditions(params):
    conditions = []
    actions_classes = set()
    param_fields = set(params.keys())
    for condition in CONDITIONS:
        if condition.REQUIRED_PARAMS.issubset(param_fields):
            conditions.append(condition(params))
            actions_classes = actions_classes | condition.ACTIONS

    return conditions, actions_classes
