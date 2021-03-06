from .group_size import GroupSizeCondition
from .level_difference_condition import LevelDifferenceCondition
from .player_type_num_difference import PlayerTypeNumDifferenceCondition
from .team_size_condition import TeamSizeCondition

CONDITIONS = (GroupSizeCondition, TeamSizeCondition, PlayerTypeNumDifferenceCondition, LevelDifferenceCondition)


def build_conditions(rules):
    conditions = []
    param_fields = set(rules.keys())
    for condition in CONDITIONS:
        if condition.get_required_rule_fields().issubset(param_fields):
            conditions.append(condition(rules))

    return conditions
