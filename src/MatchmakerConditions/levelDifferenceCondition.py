from MatchmakerActions.addDivisionAction import AddDivisionActionBase
from MatchmakerActions.removeDivisionAction import RemoveDivisionActionBase
from MatchmakerActions.swapDivisionFromQueueAction import SwapDivisionsFromQueueActionBase
from MatchmakerActions.swapDivisionsAction import SwapDivisionsActionBase
from MatchmakerConditions.condition import Condition


class LevelDifferenceCondition(Condition):
	ACTIONS = {AddDivisionActionBase, SwapDivisionsActionBase, RemoveDivisionActionBase, SwapDivisionsFromQueueActionBase}
	REQUIRED_PARAMS = {"max_level_difference", }

	def __init__(self, params):
		super().__init__(params)
		self.max_level_difference = params["max_level_difference"]

	def check(self, battle_group):
		levels = [division.level for team in battle_group.teams for division in team.divisions]
		max_level = max(levels)

		penalty = 0
		for level in levels:
			if abs(level - max_level) > self.max_level_difference:
				penalty += 1

		return penalty
