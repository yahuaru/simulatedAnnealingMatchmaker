from .condition import ICondition


class LevelDifferenceCondition(ICondition):
	def __init__(self, rules):
		super().__init__(rules)
		self.max_level_difference = rules['max_level_difference']
		self.teams_num = rules['teams_num']

	@classmethod
	def get_required_rule_fields(cls):
		return {"max_level_difference", 'teams_num'}

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
