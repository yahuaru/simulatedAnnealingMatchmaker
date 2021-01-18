import random

from MatchmakerActions.action import SimulatedAnnealingAction
from battleGroup import BattleGroup


class SwapDivisionsFromQueueAction(SimulatedAnnealingAction):
    def __init__(self, params):
        super().__init__(params)
        self.__max_team_size = params['max_team_size']
        self.__added_division = None
        self.__removed_division = None

    def execute(self, queue, battle_group):
        if not queue:
            return None

        not_empty_team = [(team_id, team) for team_id, team in enumerate(battle_group.teams) if team.size > 0]
        if not not_empty_team:
            return None

        team_id, team = random.choice(not_empty_team)
        division = random.choice(team.divisions)

        free_space = self.__max_team_size - team.size
        division_from_queue = queue.popDivisionBySize(division.size + free_space)
        if division_from_queue is None:
            return None

        new_battle_group = BattleGroup.swapDivision(battle_group, team_id, division, division_from_queue)

        self.__removed_division = division
        self.__added_division = division_from_queue

        return new_battle_group

    def on_approved(self, queue):
        queue.pushDivision(self.__removed_division)
        self.__added_division = None
        self.__removed_division = None

    def on_rejected(self, queue):
        queue.pushDivision(self.__added_division)
        self.__added_division = None
        self.__removed_division = None
