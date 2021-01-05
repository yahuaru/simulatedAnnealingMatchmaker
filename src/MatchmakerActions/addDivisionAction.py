import random

from MatchmakerActions.action import SimulatedAnnealingAction


class AddDivisionAction(SimulatedAnnealingAction):
    def __init__(self, params):
        super().__init__(params)
        self.__max_team_size = params['max_team_size']
        self.__added_division_index = -1

    def execute(self, queue, battle_group):
        if not queue:
            return False

        vacant_teams = [team for team in battle_group.teams if team.size < self.__max_team_size]
        if not vacant_teams:
            return False

        vacant_team = random.choice(vacant_teams)
        for i, (_, _, division) in enumerate(queue):
            if division.size <= (self.__max_team_size - vacant_team.size):
                self.__added_division_index = i
                vacant_team.addDivision(division)
                return True

        return False

    def on_approved(self, queue):
        queue.removeByIndex(self.__added_division_index)
        self.__added_division_index = -1

    def on_rejected(self, queue):
        self.__added_division_index = -1

