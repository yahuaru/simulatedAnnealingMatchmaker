import random

from MatchmakerActions.action import SimulatedAnnealingAction


class AddDivisionAction(SimulatedAnnealingAction):
    def __init__(self, params):
        super().__init__(params)
        self.__team_size = params['team_size']
        self.__added_division = None

    def execute(self, queue, battle_group):
        if not queue:
            return False
        vacant_teams = [team for team in battle_group.teams if team.size < self.__team_size]
        if not vacant_teams:
            return False

        vacant_team = random.choice(vacant_teams)
        acceptable_division = None
        for division in queue:
            if division.size <= (self.__team_size - vacant_team.size):
                acceptable_division = division
                break
        if acceptable_division is None:
            return False
        self.__added_division = acceptable_division
        queue.remove(self.__added_division)
        vacant_team.addDivision(self.__added_division)
        return True

    def on_approved(self, queue):
        self.__added_division = None

    def on_rejected(self, queue):
        queue.append(self.__added_division)
        self.__added_division = None
