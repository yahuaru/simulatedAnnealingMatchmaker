from battleGroup import BattleGroup, Team


class GreedMatchmaker:
	def __init__(self, team_size, teams_num):
		self.__queue = []
		self.__team_size = team_size
		self.__teams_num = teams_num

	def enqueueDivision(self, division):
		self.__queue.append(division)

	def dequeueDivision(self, division):
		self.__queue.remove(division)

	def process(self):
		battle_group = BattleGroup(Team() for _ in range(self.__teams_num))
		queue = list(self.__queue)
		division = queue.pop(0)
		battle_group = BattleGroup.addDivision(battle_group, 0, division)
		place_left = self.__team_size * self.__teams_num * sum(team.size for team in battle_group.teams)
		while place_left and queue:
			for team_id, team in enumerate(battle_group.teams):
				for division in queue:
					if division.size <= self.__team_size - team.size:
						battle_group = BattleGroup.addDivision(battle_group, team_id, division)
						queue.remove(division)
						place_left -= division
						break
		if place_left > 0:
			return None

		return battle_group
