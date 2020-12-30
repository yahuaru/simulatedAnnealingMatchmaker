from MatchmakerConditions.playerTypeNumDifferenceCondition import PlayerTypeNumDifferenceCondition
from MatchmakerConditions.teamSizeCondition import TeamSizeCondition

PARAM_FIELD_TO_CONDITION = {
    'team_size': TeamSizeCondition,
    'player_type_num_diff': PlayerTypeNumDifferenceCondition
}


def buildConditions(params):
    conditions = []
    actions = set()
    for field in params:
        if field in PARAM_FIELD_TO_CONDITION:
            conditions.append(PARAM_FIELD_TO_CONDITION[field](params))
            actions.update(PARAM_FIELD_TO_CONDITION[field].ACTIONS)
    return conditions, actions


