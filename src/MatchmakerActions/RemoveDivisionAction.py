import random

from MatchmakerActions.Action import SimulatedAnnealingAction


class RemoveDivisionAction(SimulatedAnnealingAction):
    def __init__(self, params):
        super().__init__(params)
        self.__removed_division = None

    def execute(self, queue, battle_group):
        not_empty_team = [team for team in battle_group.teams if team.size > 0]
        if not not_empty_team:
            return False

        team = random.choice(not_empty_team)
        division = random.choice(team.divisions)
        team.removeDivision(division)
        self.__removed_division = division
        return True

    def on_approved(self, queue):
        queue.append(self.__removed_division)
        self.__removed_division = None

    def on_rejected(self, queue):
        self.__removed_division = None