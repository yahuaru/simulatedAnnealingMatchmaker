from collector.conditions.level_difference_condition import LevelDifferenceCondition
from collector.conditions.player_type_num_difference import PlayerTypeNumDifferenceCondition
from collector.conditions.team_size_condition import TeamSizeCondition

CONDITIONS = (TeamSizeCondition, PlayerTypeNumDifferenceCondition, LevelDifferenceCondition)


def buildConditions(params):
    conditions = []
    param_fields = set(params.keys())
    for condition in CONDITIONS:
        if condition.get_required_rule_fields().issubset(param_fields):
            conditions.append(condition(params))

    return conditions
