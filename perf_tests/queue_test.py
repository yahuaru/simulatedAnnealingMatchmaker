import unittest
from unittest.mock import patch

import pandas as pd

from player import PlayerType
from tests.helper_functions import generateDivision

THREADS_NUM = 2
TEAMS_NUM = 4
MAX_TEAM_SIZE = 3
MIN_TEAM_SIZE = 1

SEC_PER_TICK = 0.01

ADD_TEAM_SEC = 0.5

params = {
    'common_conditions': {
        'teams_num': TEAMS_NUM,
    },
    'by_time': {
        0: {
            'conditions': {
                'min_team_size': MAX_TEAM_SIZE,
                'max_team_size': MAX_TEAM_SIZE,
                'player_type_num_diff': {
                    PlayerType.ALPHA: 0,
                    PlayerType.BETA: 0,
                    PlayerType.GAMMA: 0,
                },
            },
            'initial_temperature': 3
        },
        200: {
            'conditions': {
                'min_team_size': 1,
                'max_team_size': MAX_TEAM_SIZE,
                'team_size_equal': True,
                'player_type_num_diff': {
                    PlayerType.ALPHA: 0,
                    PlayerType.BETA: 0,
                    PlayerType.GAMMA: 0,
                },
            },
            'initial_temperature': 3,
        },
        300: {
            'conditions': {
                'min_team_size': MIN_TEAM_SIZE,
                'max_team_size': MAX_TEAM_SIZE,
                'team_size_equal': False,
            },
            'initial_temperature': 3,
        },
    }
}

DIVISIONS_NUM = 1000


class Test_SimulatedAnnealingMatchmakerQueue(unittest.TestCase):
    def setUp(self) -> None:
        self.mm = None
        self.is_finished = False
        self.processed_divisions = 0

        self.result_battle_groups = []
        self.current_time = 0

        self.battle_group_index = 0
        self.queue_size_by_time = []

    def tearDown(self) -> None:
        df = pd.DataFrame(self.result_battle_groups, columns=["battle_group_id", "battle_group_wait_time", "team_id",
                                                              "division_id", "division_enqueue_time",
                                                              "division_wait_time", "player_type"])
        df.to_csv("data/queue/battle_group_n{}_s{}_thr{}.csv".format(TEAMS_NUM, MAX_TEAM_SIZE, THREADS_NUM))
        queue_size_df = pd.DataFrame(self.queue_size_by_time, columns=["time", "size"])
        queue_size_df.to_csv("data/queue/size_n{}_s{}_thr{}.csv".format(TEAMS_NUM, MAX_TEAM_SIZE, THREADS_NUM))

    @patch("time.time", return_value=0)
    def test_processQueue(self, time_patch):
        simulatedAnnealingThread.MAX_PROCESS_TIME = 999999
        self.mm = SimulatedAnnealingMatchmaker(params, THREADS_NUM, self.onResultBattleGroup)

        tick = 0
        index = 0
        while not self.is_finished:
            self.current_time = tick * SEC_PER_TICK
            time_patch.return_value = self.current_time
            if index < DIVISIONS_NUM and index * ADD_TEAM_SEC <= self.current_time:
                division = generateDivision(index, MAX_TEAM_SIZE, enqueue_time=time_patch())
                index += 1
                self.mm.enqueueDivision(division)
                self.queue_size_by_time.append((self.current_time, len(self.mm._SimulatedAnnealingMatchmaker__queue)))
                print("size", self.current_time, len(self.mm._SimulatedAnnealingMatchmaker__queue))
            self.mm.startProcess()
            tick += 1

        self.mm.stopProcess()

    def onResultBattleGroup(self, battle_group):
        current_time = self.current_time
        self.queue_size_by_time.append((current_time, len(self.mm._SimulatedAnnealingMatchmaker__queue)))
        for i, team in enumerate(battle_group.teams):
            for division in team.divisions:
                for player in division.players:
                    self.result_battle_groups.append((self.battle_group_index,
                                                      current_time - battle_group.min_enqueue_time,
                                                      i, division.id, division.enqueue_time,
                                                      current_time - division.enqueue_time,
                                                      str(player.type)))
        self.battle_group_index += 1
        self.processed_divisions += sum([len(team.divisions) for team in battle_group.teams])
        self.is_finished = (DIVISIONS_NUM - self.processed_divisions) < TEAMS_NUM
        print(current_time, DIVISIONS_NUM - self.processed_divisions)


if __name__ == '__main__':
    unittest.main()
