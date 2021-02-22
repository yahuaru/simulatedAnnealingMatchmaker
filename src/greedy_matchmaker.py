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
		queue = list(self.__queue)
		while queue:
			battle_group = BattleGroup([Team() for _ in range(self.__teams_num)])

			import random
			division = queue.pop(random.randint(0, len(queue) - 1))
			while queue and (battle_group.teams[0].size + division.size) > self.__team_size:
				division = queue.pop(random.randint(0, len(queue) - 1))
			if (battle_group.teams[0].size + division.size) > self.__team_size:
				break
			battle_group = BattleGroup.addDivision(battle_group, 0, division)

			for team_id in range(1, self.__teams_num):
				current_all_divisions = list(queue)
				for division in current_all_divisions:
					is_fitting = True
					if battle_group.teams[team_id].size + division.size > self.__team_size:
						is_fitting = False
					else:
						for player_type, type_num in battle_group.teams[0].players_types_num.items():
							if type_num < (battle_group.teams[team_id].players_types_num[player_type] + division.players_types_num[player_type]):
								is_fitting = False
								break

					if is_fitting:
						battle_group = BattleGroup.addDivision(battle_group, team_id, division)
						queue.remove(division)
					if battle_group.teams[0].size == battle_group.teams[team_id].size:
						break
			if all(team.size == self.__team_size for team in battle_group.teams):
				for team in battle_group.teams:
					for division in team.divisions:
						self.__queue.remove(division)
				return battle_group

		return None
