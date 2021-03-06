import random

from collector.actions.action import ActionBase


class SwapDivisionsAction(ActionBase):
    def __init__(self, params):
        super().__init__(params)
        self.__max_team_size = params['max_team_size']

    def execute(self, current_time, queue, group_key, battle_group):
        if battle_group.is_empty():
            return None

        teams = [(team_id, team) for team_id, team in enumerate(battle_group.teams)]
        team_entry = random.choice(teams)
        teams.remove(team_entry)
        team_id, team = team_entry
        other_team_id, other_team = random.choice(teams)

        if team.size == 0 and other_team.size == 0:
            return None

        division = None
        if team.size != 0:
            division = random.choice(team.divisions)

        other_division = None
        if other_team.size != 0:
            other_division = random.choice(other_team.divisions)

        if division is not None and other_division is not None:
            if (division.size <= (other_division.size + self.__max_team_size - other_team.size)
                    and other_division.size <= (division.size + self.__max_team_size - team.size)):
                new_battle_group = battle_group.swap_division(current_time, team_id, division, other_division)
                new_battle_group = new_battle_group.swap_division(current_time, other_team_id, other_division, division)
                return new_battle_group
        elif division is not None and division.size <= (self.__max_team_size - other_team.size):
            new_battle_group = battle_group.remove_division(current_time, team_id, division)
            new_battle_group = new_battle_group.add_division(current_time, other_team_id, division)
            return new_battle_group
        elif other_division is not None and other_division.size <= (self.__max_team_size - team.size):
            new_battle_group = battle_group.add_division(current_time, team_id, other_division)
            new_battle_group = new_battle_group.remove_division(current_time, other_team_id, other_division)
            return new_battle_group

        return None
