from MatchmakerConditions.PlayerTypeNumDifferenceCondition import PlayerTypeNumDifferenceCondition
from MatchmakerConditions.TeamSizeCondition import TeamSizeCondition

PARAM_FIELD_TO_CONDITION = {
    'team_size': TeamSizeCondition,
    'player_type_num_diff': PlayerTypeNumDifferenceCondition
}


def buildConditions(params):
    conditions = []
    for field in params:
        if field in PARAM_FIELD_TO_CONDITION:
            conditions.append(PARAM_FIELD_TO_CONDITION[field](params))
    return conditions


