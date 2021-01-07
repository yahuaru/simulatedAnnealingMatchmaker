import unittest  # The test framework

from battleGroup import Division
from player import Player, PlayerType
from simulatedAnnealing import SimulatedAnnealingMatchmaker


class Test_SimulatedAnnealingMatchmaker(unittest.TestCase):
    def setUp(self) -> None:
        self.params = {
            'teams_num': 3,
            'by_time': {
                0: {
                    'min_team_size': 3,
                    'max_team_size': 3,
                    'player_type_num_diff': {
                        PlayerType.ALPHA: 0,
                        PlayerType.BETA: 0,
                        PlayerType.GAMMA: 0,
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
        self.mm = SimulatedAnnealingMatchmaker(self.params, self.onResultBattleGroup)
        self.result_battle_group = None

    def tearDown(self) -> None:
        self.mm.clear()
        self.result_battle_group = None

    # T: D(ALPHA), D(BETA), D(GAMMA)
    # T: D(ALPHA), D(BETA), D(GAMMA)
    # T: D(ALPHA), D(BETA), D(GAMMA)
    def test_processBattleGroup(self):
        index = 0
        for i in range(self.params['teams_num']):
            player = Player(PlayerType.ALPHA, 0, 0)
            index += 1
            division = Division(index)
            division.addPlayer(player)
            self.mm.enqueueDivision(division)

        for i in range(self.params['teams_num']):
            player = Player(PlayerType.BETA, 0, 0)
            index += 1
            division = Division(index)
            division.addPlayer(player)
            self.mm.enqueueDivision(division)

        for i in range(self.params['teams_num']):
            player = Player(PlayerType.GAMMA, 0, 0)
            index += 1
            division = Division(index)
            division.addPlayer(player)
            self.mm.enqueueDivision(division)

        self.mm.startProcess()
        self.mm.waitForCompletion()

        self.assertIsNotNone(self.result_battle_group)

        self.assertEqual(len(self.mm._SimulatedAnnealingMatchmaker__queue), 0)

        self.assertEqual(len(self.result_battle_group.teams), self.params['teams_num'])

        for team in self.result_battle_group.teams:
            self.assertEqual(team.size, self.params['by_time'][0]['max_team_size'])
        for i, team in enumerate(self.result_battle_group.teams):
            for otherTeam in self.result_battle_group.teams[i:]:
                for playerType in list(PlayerType):
                    type_num = team.players_types_num[playerType]
                    other_type_num = otherTeam.players_types_num[playerType]
                    delta_type = abs(other_type_num - type_num)
                    max_type_diff = self.params['by_time'][0]['player_type_num_diff'][playerType]
                    self.assertLessEqual(delta_type, max_type_diff)

    def onResultBattleGroup(self, battle_group):
        self.result_battle_group = battle_group
        self.assertNotIn(battle_group, self.mm._SimulatedAnnealingMatchmaker__queue,
                         self.mm._SimulatedAnnealingMatchmaker__queue._SimulatedAnnealingMatchmakerQueue__queue)

    # T: D(GAMMA, BETA), D(ALPHA)
    # T: D(BETA, ALPHA), D(GAMMA)
    # T: D(ALPHA, BETA, GAMMA)
    def test_processDifferentSizeDivisionsBattleGroup(self):
        self.mm.enqueueDivision(Division(0, [Player(PlayerType.GAMMA, 0, 0), Player(PlayerType.BETA, 0, 0)]))
        self.mm.enqueueDivision(Division(1, [Player(PlayerType.ALPHA, 0, 0)]))
        self.mm.enqueueDivision(Division(2, [Player(PlayerType.BETA, 0, 0), Player(PlayerType.ALPHA, 0, 0)]))
        self.mm.enqueueDivision(Division(3, [Player(PlayerType.GAMMA, 0, 0)]))
        self.mm.enqueueDivision(Division(4, [Player(PlayerType.ALPHA, 0, 0), Player(PlayerType.BETA, 0, 0),
                                             Player(PlayerType.GAMMA, 0, 0)]))

        self.mm.startProcess()
        self.mm.waitForCompletion()

        self.assertIsNotNone(self.result_battle_group)

        self.assertEqual(len(self.mm._SimulatedAnnealingMatchmaker__queue), 0)

        self.assertEqual(len(self.result_battle_group.teams), self.params['teams_num'])

        for team in self.result_battle_group.teams:
            self.assertEqual(team.size, self.params['by_time'][0]['max_team_size'])
        for i, team in enumerate(self.result_battle_group.teams):
            for otherTeam in self.result_battle_group.teams[i:]:
                for playerType in list(PlayerType):
                    type_num = team.players_types_num[playerType]
                    other_type_num = otherTeam.players_types_num[playerType]
                    delta_type = abs(other_type_num - type_num)
                    max_type_diff = self.params['by_time'][0]['player_type_num_diff'][playerType]
                    self.assertLessEqual(delta_type, max_type_diff)

    # def test_waitTimeRules(self):
    #     index = 0
    #     for i in range(3):
    #         player = Player(PlayerType.ALPHA, 0, 0)
    #         index += 1
    #         division = Division(index)
    #         division.addPlayer(player)
    #         self.mm.enqueueDivision(division)
    #
    #     for i in range(3):
    #         player = Player(PlayerType.BETA, 0, 0)
    #         index += 1
    #         division = Division(index)
    #         division.addPlayer(player)
    #         self.mm.enqueueDivision(division)
    #
    #     for i in range(3):
    #         player = Player(PlayerType.GAMMA, 0, 0)
    #         index += 1
    #         division = Division(index)
    #         division.addPlayer(player)
    #         self.mm.enqueueDivision(division)
    #
    #     for i in range(3):
    #         player = Player(PlayerType.ALPHA, 0, 0)
    #         index += 1
    #         division = Division(index)
    #         division.addPlayer(player)
    #         self.mm.enqueueDivision(division)
    #
    #     for i in range(3):
    #         player = Player(PlayerType.BETA, 0, 0)
    #         index += 1
    #         division = Division(index)
    #         division.addPlayer(player)
    #         self.mm.enqueueDivision(division)
    #
    #     successful = False
    #     bg = None
    #     self.mm.startProcess()
    #     while not successful:
    #         successful, bg = self.mm.processBattleGroups(0)
    #
    #     self.assertTrue(successful)
    #     self.assertIsNotNone(bg)
    #
    #     self.assertEqual(len(self.mm._SimulatedAnnealingMatchmaker__queue), 6)
    #
    #     self.assertEqual(len(bg.teams), self.params['teams_num'])
    #
    #     for team in bg.teams:
    #         self.assertEqual(team.size, self.params['by_time'][0]['max_team_size'])
    #     for i, team in enumerate(bg.teams):
    #         for otherTeam in bg.teams[i:]:
    #             for playerType in list(PlayerType):
    #                 type_num = team.players_types_num[playerType]
    #                 other_type_num = otherTeam.players_types_num[playerType]
    #                 delta_type = abs(other_type_num - type_num)
    #                 max_type_diff = self.params['by_time'][0]['player_type_num_diff'][playerType]
    #                 self.assertLessEqual(delta_type, max_type_diff)
    #
    #     successful = False
    #     bg = None
    #     self.mm.startProcess()
    #     while not successful:
    #         successful, bg = self.mm.processBattleGroups(2)
    #
    #     self.assertTrue(successful)
    #     self.assertIsNotNone(bg)
    #
    #     self.assertEqual(len(self.mm._SimulatedAnnealingMatchmaker__queue), 0)
    #
    #     self.assertEqual(len(bg.teams), self.params['teams_num'])
    #
    #     for team in bg.teams:
    #         self.assertLessEqual(team.size, self.params['by_time'][2]['max_team_size'])
    #         self.assertGreaterEqual(team.size, self.params['by_time'][2]['min_team_size'])


if __name__ == '__main__':
    unittest.main()
