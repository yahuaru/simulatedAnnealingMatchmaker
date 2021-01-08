import random

from MatchmakerActions.action import SimulatedAnnealingAction


class SwapDivisionsFromQueueAction(SimulatedAnnealingAction):
    def __init__(self, params):
        super().__init__(params)
        self.__max_team_size = params['max_team_size']
        self.__added_division = None
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
        division_from_queue = queue.popDivisionBySize(division.size + free_space)
        if division_from_queue is None:
            return False

        team.removeDivision(division)
        self.__removed_division = division
        team.addDivision(division_from_queue)
        self.__added_division = division_from_queue
        return True

    def on_approved(self, queue):
        queue.pushDivision(self.__removed_division)
        self.__added_division = None
        self.__removed_division = None

    def on_rejected(self, queue):
        queue.pushDivision(self.__added_division)
        self.__added_division = None
        self.__removed_division = None
