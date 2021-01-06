import random

from MatchmakerActions.action import SimulatedAnnealingAction


class SwapDivisionsFromQueueAction(SimulatedAnnealingAction):
    def __init__(self, params):
        super().__init__(params)
        self.__max_team_size = params['max_team_size']
        self.__added_division_index = -1
        self.__removed_division = None

    def execute(self, queue, battle_group):
        if not queue:
            return False

        not_empty_team = [team for team in battle_group.teams if team.size > 0]
        if not not_empty_team:
            return False

        team = random.choice(not_empty_team)
        division = random.choice(team.divisions)

        free_space = self.__max_team_size - team.size
        for i, entry in enumerate(queue):
            if entry.division.size <= (division.size + free_space):
                team.removeDivision(division)
                self.__removed_division = division
                team.addDivision(entry.division)
                self.__added_division_index = i
                return True

        return False

    def on_approved(self, queue):
        queue.removeByIndex(self.__added_division_index)
        queue.pushDivision(self.__removed_division)
        self.__added_division_index = -1
        self.__removed_division = None

    def on_rejected(self, queue):
        self.__added_division_index = -1
        self.__removed_division = None
