from battle_group.team import Team


class BattleGroup:
    def __init__(self, teams=None, current_time=0):
        self.teams = teams if teams is not None else []
        self.wait_time = 0
        if not self.is_empty():
            enqueue_time = min(team.min_enqueue_time for team in self.teams if team.size != 0)
            self.wait_time = current_time - enqueue_time

    def is_empty(self):
        return not any(team.size != 0 for team in self.teams)

    def size(self):
        return len(self.teams)

    def add_division(self, current_time, team_id, division):
        new_teams = self.teams.copy()
        new_team = new_teams[team_id] = new_teams[team_id].copy()
        new_team.add_division(division)
        return BattleGroup(new_teams, current_time)

    def remove_division(self, current_time, team_id, division):
        new_teams = self.teams.copy()
        new_team = new_teams[team_id] = self.teams[team_id].copy()
        new_team.remove_division(division)
        return BattleGroup(new_teams, current_time)

    def swap_division(self, current_time, team_id, removed_division, add_division):
        new_teams = self.teams.copy()
        new_team = new_teams[team_id] = new_teams[team_id].copy()
        new_team.remove_division(removed_division)
        new_team.add_division(add_division)
        return BattleGroup(new_teams, current_time)

    def extend_size(self, current_time, teams_num):
        teams = self.teams.copy()
        teams.extend([Team() for _ in range(len(teams), teams_num)])
        return BattleGroup(teams, current_time)

    def remove_team(self, current_time, team_id):
        teams = self.teams.copy()
        del teams[team_id]
        return BattleGroup(teams, current_time)

    def __repr__(self) -> str:
        teams_repr = ""
        for team in self.teams:
            teams_repr += "\t{}\n".format(team)
        return "battle_group[\n{}\n\t]".format(teams_repr)

    def __iter__(self):
        return iter(self.teams)
