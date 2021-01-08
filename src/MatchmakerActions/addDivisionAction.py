import random

from MatchmakerActions.action import SimulatedAnnealingAction


class AddDivisionAction(SimulatedAnnealingAction):
    def __init__(self, params):
        super().__init__(params)
        self.__max_team_size = params['max_team_size']
        self.__added_division = None

    def execute(self, queue, battle_group):
        if not queue:
            return False

        vacant_teams = [team for team in battle_group.teams if team.size < self.__max_team_size]
        if not vacant_teams:
            return False

        vacant_team = random.choice(vacant_teams)
        division_from_queue = queue.popDivisionBySize(self.__max_team_size - vacant_team.size)
        if division_from_queue is None:
            return False

        self.__added_division = division_from_queue
        vacant_team.addDivision(division_from_queue)
        return True

    def on_approved(self, queue):
        self.__added_division = None

    def on_rejected(self, queue):
        queue.pushDivision(self.__added_division)
        self.__added_division = None

