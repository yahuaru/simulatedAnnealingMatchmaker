import time
import unittest
from unittest.mock import patch

import simulatedAnnealingThread
from player import PlayerType
from simulatedAnnealing import SimulatedAnnealingMatchmaker
from tests.helper_functions import generateDivision
import pandas as pd

THREADS_NUM = 1
TEAMS_NUM = 4
MAX_TEAM_SIZE = 3
MIN_TEAM_SIZE = 1

SEC_PER_TICK = 0.01

ADD_TEAM_SEC = 0.5

DIVISIONS_NUM = 1000

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
    }
}


class Test_SimulatedAnnealingMatchmakerQueue(unittest.TestCase):
    def setUp(self) -> None:
        pass

    def tearDown(self) -> None:
        pass

    @patch("time.time", return_value=0)
    def test_processQueue(self, time_patch):
        simulatedAnnealingThread.MAX_PROCESS_TIME = 999999

        mm = SimulatedAnnealingMatchmaker(params, THREADS_NUM, self.onResultBattleGroup)
        for index in range(1000):
            division = generateDivision(index, MAX_TEAM_SIZE, enqueue_time=time_patch(), min_level=1, max_level=6)
            mm.enqueueDivision(division)
        mm.startProcess()
        mm.waitForCompletion()

    def onResultBattleGroup(self, battle_group):
        print(battle_group)


if __name__ == '__main__':
    unittest.main()
