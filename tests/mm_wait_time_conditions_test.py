import time
import unittest  # The test framework
from unittest.mock import patch

from battleGroup import Division
from player import Player, PlayerType
from simulatedAnnealing import SimulatedAnnealingMatchmaker
from simulatedAnnealingQueue import QueueEntry

THREADS_NUM = 1

TEAMS_NUM = 3
MAX_TEAM_SIZE = 3
MIN_TEAM_SIZE = 2

SECOND_TRY_TIME = 20


class Test_SimulatedAnnealingMatchmaker(unittest.TestCase):
    def setUp(self) -> None:
        self.params = {
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
                SECOND_TRY_TIME: {
                    'conditions': {
                        'min_team_size': MIN_TEAM_SIZE,
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
            }
        }
        self.mm = SimulatedAnnealingMatchmaker(self.params, THREADS_NUM, self.onResultBattleGroup)
        self.result_battle_group = None

    def tearDown(self) -> None:
        self.result_battle_group = None

    def onResultBattleGroup(self, battle_group):
        self.result_battle_group = battle_group

    # T: D(ALPHA), D(BETA), D(GAMMA)
    # T: D(ALPHA), D(BETA), D(GAMMA)
    # T: D(ALPHA), D(BETA), D(GAMMA)
    @patch("time.time", return_value=0)
    def test_waitTimeConditions(self, time_patch):
        index = 0
        for i in range(TEAMS_NUM):
            player = Player(PlayerType.ALPHA, 0)
            index += 1
            division = Division(index)
            division.addPlayer(player)
            self.mm.enqueueDivision(division)

        for i in range(TEAMS_NUM):
            player = Player(PlayerType.BETA, 0)
            index += 1
            division = Division(index)
            division.addPlayer(player)
            self.mm.enqueueDivision(division)

        for i in range(TEAMS_NUM):
            player = Player(PlayerType.GAMMA, 0)
            index += 1
            division = Division(index)
            division.addPlayer(player)
            self.mm.enqueueDivision(division)

        for i in range(TEAMS_NUM):
            player = Player(PlayerType.ALPHA, 0)
            index += 1
            division = Division(index)
            division.addPlayer(player)
            self.mm.enqueueDivision(division)

        for i in range(TEAMS_NUM):
            player = Player(PlayerType.BETA, 0)
            index += 1
            division = Division(index)
            division.addPlayer(player)
            self.mm.enqueueDivision(division)

        self.mm.startProcess()
        self.mm.waitForCompletion()

        self.assertIsNotNone(self.result_battle_group)

        for team in self.result_battle_group.teams:
            for division in team.divisions:
                entry = QueueEntry(division.enqueue_time, division.id, division)
                self.assertNotIn(entry, self.mm._SimulatedAnnealingMatchmaker__queue,
                                 self.mm._SimulatedAnnealingMatchmaker__queue._SimulatedAnnealingMatchmakerQueue__queue)

        self.assertEqual(6, len(self.mm._SimulatedAnnealingMatchmaker__queue))

        self.assertEqual(TEAMS_NUM, len(self.result_battle_group.teams))

        for team in self.result_battle_group.teams:
            self.assertEqual(team.size, MAX_TEAM_SIZE)
        for i, team in enumerate(self.result_battle_group.teams):
            for otherTeam in self.result_battle_group.teams[i:]:
                for playerType in list(PlayerType):
                    type_num = team.players_types_num[playerType]
                    other_type_num = otherTeam.players_types_num[playerType]
                    delta_type = abs(other_type_num - type_num)
                    max_type_diff = self.params['by_time'][0]['conditions']['player_type_num_diff'][playerType]
                    self.assertLessEqual(delta_type, max_type_diff)

        time_patch.return_value = SECOND_TRY_TIME
        self.mm.startProcess()
        self.mm.waitForCompletion()

        self.assertIsNotNone(self.result_battle_group)

        self.assertEqual(len(self.mm._SimulatedAnnealingMatchmaker__queue), 0)

        self.assertEqual(len(self.result_battle_group.teams), TEAMS_NUM)

        for team in self.result_battle_group.teams:
            self.assertLessEqual(team.size, MAX_TEAM_SIZE)
            self.assertGreaterEqual(team.size, MIN_TEAM_SIZE)


if __name__ == '__main__':
    unittest.main()
