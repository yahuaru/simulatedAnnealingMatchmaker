from player import PlayerType


class Division:
    def __init__(self, division_id, players=None, enqueue_time=0.0):
        self.id = division_id
        self.players = players if players is not None else []
        self.size = len(self.players)
        self.players_types_num = {playerType: 0 for playerType in list(PlayerType)}
        self.max_level = 0
        for player in self.players:
            self.players_types_num[player.type] += 1
            self.max_level = max(self.max_level, player.level)
        self.enqueue_time = enqueue_time

    def add_player(self, player):
        self.size += 1
        self.players.append(player)
        self.players_types_num[player.type] += 1
        self.max_level = max(self.max_level, player.level)

    def __repr__(self):
        res = "Division(players={}, playersTypeNum={}, maxLevel={}, size={})"
        return res.format(self.players, self.players_types_num, self.max_level, self.size)


class Team:
    def __init__(self, division=None) -> None:
        self.divisions = division if division is not None else []
        self.players_types_num = {playerType: 0 for playerType in list(PlayerType)}
        self.size = 0
        self.min_enqueue_time = min(division.enqueue_time for division in self.divisions) if self.divisions else 0
        self.max_level = 0
        for division in self.divisions:
            for playerType in list(PlayerType):
                self.players_types_num[playerType] += division.players_types_num[playerType]
            self.size += division.size
            self.max_level = max(self.max_level, division.max_level)

    def add_division(self, division):
        self.divisions.append(division)
        for playerType in list(PlayerType):
            self.players_types_num[playerType] += division.players_types_num[playerType]
        self.size += division.size
        self.min_enqueue_time = min(division.enqueue_time for division in self.divisions)
        self.max_level = max(self.max_level, division.max_level)

    def remove_division(self, division):
        self.divisions.remove(division)
        for playerType in list(PlayerType):
            self.players_types_num[playerType] -= division.players_types_num[playerType]
        self.size -= division.size
        self.min_enqueue_time = min(d.enqueue_time for d in self.divisions) if self.divisions else 0
        self.max_level = max(d.max_level for d in self.divisions) if self.divisions else 0

    def copy(self):
        team = Team()
        team.divisions = list(self.divisions)
        team.players_types_num = self.players_types_num.copy()
        team.size = self.size
        team.min_enqueue_time = self.min_enqueue_time
        team.max_level = self.max_level
        return team

    def __repr__(self) -> str:
        res = "Team(divisions:{}, playersTypeNum:{}, size:{}, min_enqueue_time:{})"
        return res.format(self.divisions, self.players_types_num, self.size, self.min_enqueue_time)

    def __iter__(self):
        return iter(self.divisions)


class BattleGroup:
    def __init__(self, teams=None, current_time=0):
        self.teams = teams if teams is not None else []
        self.wait_time = 0
        self.update_wait_time(current_time)

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

    def update_wait_time(self, current_time):
        if self.is_empty():
            self.wait_time = 0
            return

        enqueue_time = min(team.min_enqueue_time for team in self.teams if team.size != 0)
        self.wait_time = current_time - enqueue_time

    def __repr__(self) -> str:
        teams_repr = ""
        for team in self.teams:
            teams_repr += "\t{}\n".format(team)
        return "BattleGroup[\n{}\n\t]".format(teams_repr)

    def __iter__(self):
        return iter(self.teams)
