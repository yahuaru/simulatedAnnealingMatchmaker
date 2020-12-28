import random

from MatchmakerActions.Action import SimulatedAnnealingAction


class SwapDivisionsAction(SimulatedAnnealingAction):
    def __init__(self, params):
        super().__init__(params)
        self.__team_size = params['team_size']

    def execute(self, queue, battle_group):
        teams = list(battle_group.teams)
        team = random.choice(teams)
        teams.remove(team)
        other_team = random.choice(teams)

        if team.size == 0 and other_team.size == 0:
            return False

        division = None
        if team.size != 0:
            division = random.choice(team.divisions)

        other_division = None
        if other_team.size != 0:
            other_division = random.choice(other_team.divisions)

        if division is not None and other_division is not None:
            if (division.size <= (other_division.size + self.__team_size - other_team.size)
                    and other_division.size <= (division.size + self.__team_size - team.size)):
                other_team.removeDivision(other_division)
                team.removeDivision(division)

                other_team.addDivision(division)
                team.addDivision(other_division)

                return True
        elif division is not None and division.size <= (self.__team_size - other_team.size):
            team.removeDivision(division)
            other_team.addDivision(division)
            return True
        elif other_division is not None and other_division.size <= (self.__team_size - team.size):
            other_team.removeDivision(other_division)
            team.addDivision(other_division)
            return True

        return False