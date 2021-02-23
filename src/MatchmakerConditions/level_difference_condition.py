from MatchmakerActions.add_division_action import AddDivisionActionBase
from MatchmakerActions.remove_division_action import RemoveDivisionActionBase
from MatchmakerActions.swap_division_from_queue_action import SwapDivisionsFromQueueActionBase
from MatchmakerActions.swap_divisions_action import SwapDivisionsActionBase
from MatchmakerConditions.condition import Condition


class LevelDifferenceCondition(Condition):
	ACTIONS = {AddDivisionActionBase, SwapDivisionsActionBase, RemoveDivisionActionBase, SwapDivisionsFromQueueActionBase}
	REQUIRED_PARAMS = {"by_level", }

	def __init__(self, params):
		super().__init__(params)
		self.max_level_difference = params['by_level']['max_level_difference']
		self.teams_num = params['teams_num']

	def check(self, battle_group):
		levels = [division.max_level for team in battle_group.teams for division in team.divisions]
		if not levels:
			return self.max_level_difference * self.teams_num

		max_level = max(levels)

		penalty = 0
		for level in levels:
			if abs(level - max_level) > self.max_level_difference:
				penalty += 1

		return penalty
