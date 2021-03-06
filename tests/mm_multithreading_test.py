import time
import unittest

from player import PlayerType
from tests.helper_functions import generate_division

MAX_DIVISION_SIZE = 3
TEAMS_NUM = 4

THREADS_NUM = 2


class Test_MultithreadingMatchmaker(unittest.TestCase):
    def setUp(self) -> None:
        self.params = {
            'common_conditions':
            {
                'teams_num': TEAMS_NUM,
            },
            'by_time': {
                0: {
                    'conditions': {
                        'min_team_size': 3,
                        'max_team_size': MAX_DIVISION_SIZE,
                        'player_type_num_diff': {
                            PlayerType.ALPHA: 0,
                            PlayerType.BETA: 0,
                            PlayerType.GAMMA: 0,
                        },
                    },
                    'initial_temperature': 3
                },
                0.5: {
                    'conditions': {
                        'min_team_size': 2,
                        'max_team_size': MAX_DIVISION_SIZE,
                        'team_size_equal': True,
                        'player_type_num_diff': {
                            PlayerType.ALPHA: 0,
                            PlayerType.BETA: 0,
                            PlayerType.GAMMA: 0,
                        },
                    },
                    'initial_temperature': 3
                },
                1: {
                    'conditions': {
                        'min_team_size': 1,
                        'max_team_size': MAX_DIVISION_SIZE,
                        'team_size_equal': False,
                    },
                    'initial_temperature': 3
                },
            }
        }
        self.mm = SimulatedAnnealingMatchmaker(self.params, THREADS_NUM, self.onResultBattleGroup)
        self.start_time = 0
        self.is_finished = False
        self.result_battle_group = None

    def tearDown(self) -> None:
        self.result_battle_group = None

    def test_processBattleGroup(self):
        index = 0
        for i in range(1000):
            division = generate_division(index, MAX_DIVISION_SIZE, enqueue_time=time.time())
            self.mm.enqueue_division(division)
            index += 1

        self.start_time = time.time()
        while not self.is_finished:
            self.mm.startProcess()
            self.mm.waitForCompletion()
            self.is_finished = len(self.mm._SimulatedAnnealingMatchmaker__queue) < TEAMS_NUM

    def onResultBattleGroup(self, battle_group):
        self.result_battle_group = battle_group
        self.assertIsNotNone(self.result_battle_group)
        self.assertEqual(len(self.result_battle_group.teams), TEAMS_NUM)
        for team in battle_group.teams:
            for division in team.divisions:
                entry = QueueEntry(division.enqueue_time, division.id, division)
                self.assertNotIn(entry, self.mm._SimulatedAnnealingMatchmaker__queue,
                                 self.mm._SimulatedAnnealingMatchmaker__queue._SimulatedAnnealingMatchmakerQueue__queue)

        self.is_finished = len(self.mm._SimulatedAnnealingMatchmaker__queue) < TEAMS_NUM


if __name__ == '__main__':
    unittest.main()
