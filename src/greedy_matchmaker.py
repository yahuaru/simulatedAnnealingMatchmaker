import random

from battleGroup import BattleGroup, Team


class GreedyMatchmaker:
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
		while queue:
			division = queue.pop(random.randint(0, len(queue) - 1))
			battle_group = BattleGroup.addDivision(battle_group, 0, division)
			for team_id in range(self.__teams_num):
				team_size = battle_group.teams[team_id].size
				current_queue = list(queue)
				for division in current_queue:
					if division.size <= self.__team_size - team_size:
						battle_group = BattleGroup.addDivision(battle_group, team_id, division)
						queue.remove(division)
						team_size = battle_group.teams[team_id].size
						if team_size == self.__team_size:
							break

			if all(team.size == self.__team_size for team in battle_group.teams):
				for team in battle_group.teams:
					for division in team.divisions:
						self.__queue.remove(division)
				return battle_group
		return None
