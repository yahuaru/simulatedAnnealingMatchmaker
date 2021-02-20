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
		isSuccessful = False
		while isSuccessful and queue:
			battle_group = BattleGroup([Team() for _ in range(self.__teams_num)])

			division = queue.pop(0)
			while queue and (battle_group.teams[0].size + division.size()) > self.__team_size:
				division = queue.pop(0)
			if (battle_group.teams[0].size + division.size()) > self.__team_size:
				break
			battle_group = BattleGroup.addDivision(battle_group, 0, division)

			isSuccessful = False
			for team_id, team in enumerate(battle_group.teams[1:], 1):
				isSuccessful = False
				currentAllDivisions = list(queue)
				for division in currentAllDivisions:
					divisionShipType = division.getShipTypeNum()
					isFitting = True
					for player_type, type_num in battle_group.teams[0].players_types_num.iteritems():
						if type_num < (team.players_types_num[player_type] + divisionShipType[player_type]):
							isFitting = False
							break

					if isFitting:
						battle_group = BattleGroup.addDivision(battle_group, team_id, team.addDivision(division))
						queue.remove(division)
					if battle_group[0].team_size == team.team_size:
						isSuccessful = True
						break
				if not isSuccessful:
					break

			if isSuccessful:
				return battle_group

		return battle_group
