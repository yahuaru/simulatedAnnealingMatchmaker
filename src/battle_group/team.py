from player import PlayerType


class Team:
    def __init__(self, division=None) -> None:
        self.divisions = division if division is not None else []
        self.players_types_num = {playerType: 0 for playerType in PlayerType}
        self.size = 0
        self.min_enqueue_time = min(division.enqueue_time for division in self.divisions) if self.divisions else 0
        self.max_level = 0
        for division in self.divisions:
            for playerType in PlayerType:
                self.players_types_num[playerType] += division.players_types_num[playerType]
            self.size += division.size
            self.max_level = max(self.max_level, division.max_level)

    def add_division(self, division):
        self.divisions.append(division)
        for playerType in PlayerType:
            self.players_types_num[playerType] += division.players_types_num[playerType]
        self.size += division.size
        self.min_enqueue_time = min(division.enqueue_time for division in self.divisions)
        self.max_level = max(self.max_level, division.max_level)

    def remove_division(self, division):
        self.divisions.remove(division)
        for playerType in PlayerType:
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