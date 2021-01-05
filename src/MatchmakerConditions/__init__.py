from MatchmakerConditions.playerTypeNumDifferenceCondition import PlayerTypeNumDifferenceCondition
from MatchmakerConditions.teamSizeCondition import TeamSizeCondition

CONDITIONS = (TeamSizeCondition, PlayerTypeNumDifferenceCondition)


def buildConditions(params):
    conditions = []
    actions_classes = set()
    param_fields = set(params.keys())
    for condition in CONDITIONS:
        if condition.REQUIRED_PARAMS.issubset(param_fields):
            conditions.append(condition(params))
            actions_classes = actions_classes | condition.ACTIONS

    actions = []
    for action_class in actions_classes:
        actions.append(action_class(params))
    return conditions, actions
