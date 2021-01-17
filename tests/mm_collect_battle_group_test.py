import unittest  # The test framework

from battleGroup import Division
from player import Player, PlayerType
from simulatedAnnealing import SimulatedAnnealingMatchmaker

THREADS_NUM = 1

TEAMS_NUM = 3
TEAM_SIZE = 3


class Test_CollectBattleGroup(unittest.TestCase):
    def setUp(self) -> None:
        self.params = {
            'common_conditions': {
                'teams_num': TEAMS_NUM,
            },
            'by_time': {
                0: {
                    'conditions': {
                        'min_team_size': TEAM_SIZE,
                        'max_team_size': TEAM_SIZE,
                        'player_type_num_diff': {
                            PlayerType.ALPHA: 0,
                            PlayerType.BETA: 0,
                            PlayerType.GAMMA: 0,
                        },
                    },
                    'initial_temperature': 3
                },
                # 2: {
                #     'min_team_size': 2,
                #     'max_team_size': 3,
                #     'team_size_equal': False,
                #     'initial_temperature': 3
                # },
            }
        }
        self.mm = SimulatedAnnealingMatchmaker(self.params, THREADS_NUM, self.onResultBattleGroup)
        self.result_battle_group = None

    def tearDown(self) -> None:
        self.mm.clear()
        self.result_battle_group = None

    def onResultBattleGroup(self, battle_group):
        self.result_battle_group = battle_group

    # T: D(ALPHA), D(BETA), D(GAMMA)
    # T: D(ALPHA), D(BETA), D(GAMMA)
    # T: D(ALPHA), D(BETA), D(GAMMA)
    def test_processBattleGroup(self):
        index = 0
        for i in range(TEAMS_NUM):
            player = Player(PlayerType.ALPHA)
            index += 1
            division = Division(index)
            division.addPlayer(player)
            self.mm.enqueueDivision(division)

        for i in range(TEAMS_NUM):
            player = Player(PlayerType.BETA)
            index += 1
            division = Division(index)
            division.addPlayer(player)
            self.mm.enqueueDivision(division)

        for i in range(TEAMS_NUM):
            player = Player(PlayerType.GAMMA)
            index += 1
            division = Division(index)
            division.addPlayer(player)
            self.mm.enqueueDivision(division)

        self.mm.startProcess()
        self.mm.waitForCompletion()

        self.assertIsNotNone(self.result_battle_group)

        self.assertEqual(0, len(self.mm._SimulatedAnnealingMatchmaker__queue))

        self.assertEqual(TEAMS_NUM, len(self.result_battle_group.teams))

        for team in self.result_battle_group.teams:
            self.assertEqual(TEAM_SIZE, team.size)
        for i, team in enumerate(self.result_battle_group.teams):
            for otherTeam in self.result_battle_group.teams[i:]:
                for playerType in list(PlayerType):
                    type_num = team.players_types_num[playerType]
                    other_type_num = otherTeam.players_types_num[playerType]
                    delta_type = abs(other_type_num - type_num)
                    max_type_diff = self.params['by_time'][0]['conditions']['player_type_num_diff'][playerType]
                    self.assertLessEqual(delta_type, max_type_diff)

    # T: D(GAMMA, BETA), D(ALPHA)
    # T: D(BETA, ALPHA), D(GAMMA)
    # T: D(ALPHA, BETA, GAMMA)
    def test_processDifferentSizeDivisionsBattleGroup(self):
        self.mm.enqueueDivision(Division(0, [Player(PlayerType.GAMMA), Player(PlayerType.BETA)]))
        self.mm.enqueueDivision(Division(1, [Player(PlayerType.ALPHA)]))
        self.mm.enqueueDivision(Division(2, [Player(PlayerType.BETA), Player(PlayerType.ALPHA)]))
        self.mm.enqueueDivision(Division(3, [Player(PlayerType.GAMMA)]))
        self.mm.enqueueDivision(Division(4, [Player(PlayerType.ALPHA), Player(PlayerType.BETA),
                                             Player(PlayerType.GAMMA)]))

        self.mm.startProcess()
        self.mm.waitForCompletion()

        self.assertIsNotNone(self.result_battle_group)

        self.assertEqual(len(self.mm._SimulatedAnnealingMatchmaker__queue), 0)

        self.assertEqual(len(self.result_battle_group.teams), TEAMS_NUM)

        for team in self.result_battle_group.teams:
            self.assertEqual(team.size, TEAM_SIZE)
        for i, team in enumerate(self.result_battle_group.teams):
            for otherTeam in self.result_battle_group.teams[i:]:
                for playerType in list(PlayerType):
                    type_num = team.players_types_num[playerType]
                    other_type_num = otherTeam.players_types_num[playerType]
                    delta_type = abs(other_type_num - type_num)
                    max_type_diff = self.params['by_time'][0]['conditions']['player_type_num_diff'][playerType]
                    self.assertLessEqual(delta_type, max_type_diff)


if __name__ == '__main__':
    unittest.main()
