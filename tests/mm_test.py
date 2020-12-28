import unittest  # The test framework

from BattleGroup import Division
from player import Player, PlayerType
from simulatedAnnealing import SimulatedAnnealingMatchmaker


class Test_SimulatedAnnealingMatchmaker(unittest.TestCase):
    def setUp(self) -> None:
        self.params = {
            'teams_num': 3,
            'team_size': 3,
            'player_type_num_diff': {
                PlayerType.ALPHA: 0,
                PlayerType.BETA: 0,
                PlayerType.GAMMA: 0,
            },
            'initial_temperature': 3
        }
        self.mm = SimulatedAnnealingMatchmaker(self.params)
        self.mm.initProcess()

    def tearDown(self) -> None:
        self.mm.cleanup()

    def test_processBattleGroup(self):
        for i in range(self.params['teams_num']):
            player = Player(PlayerType.ALPHA, 0, 0)
            division = Division()
            division.addPlayer(player)
            self.mm.enqueueDivision(division)

        for i in range(self.params['teams_num']):
            player = Player(PlayerType.BETA, 0, 0)
            division = Division()
            division.addPlayer(player)
            self.mm.enqueueDivision(division)

        for i in range(self.params['teams_num']):
            player = Player(PlayerType.GAMMA, 0, 0)
            division = Division()
            division.addPlayer(player)
            self.mm.enqueueDivision(division)

        successful = False
        bg = None
        while not successful:
            successful, bg = self.mm.processBattleGroups()

        self.assertTrue(successful)
        self.assertIsNotNone(bg)

        self.assertEqual(len(self.mm.queue), 0)

        self.assertEqual(len(bg.teams), self.params['teams_num'])

        for team in bg.teams:
            self.assertEqual(team.size, self.params['team_size'])
        for i, team in enumerate(bg.teams):
            for otherTeam in bg.teams[i:]:
                for playerType in list(PlayerType):
                    type_num = team.playersTypesNum[playerType]
                    other_type_num = otherTeam.playersTypesNum[playerType]
                    delta_type = abs(other_type_num - type_num)
                    max_type_diff = self.params['player_type_num_diff'][playerType]
                    self.assertLessEqual(delta_type, max_type_diff)

    # T: D(GAMMA, BETA), D(ALPHA)
    # T: D(BETA, ALPHA), D(GAMMA)
    # T: D(ALPHA, BETA, GAMMA)
    def test_processDifferentSizeDivisionsBattleGroup(self):
        self.mm.enqueueDivision(Division([Player(PlayerType.GAMMA, 0, 0), Player(PlayerType.BETA, 0, 0)]))
        self.mm.enqueueDivision(Division([Player(PlayerType.ALPHA, 0, 0)]))
        self.mm.enqueueDivision(Division([Player(PlayerType.BETA, 0, 0), Player(PlayerType.ALPHA, 0, 0)]))
        self.mm.enqueueDivision(Division([Player(PlayerType.GAMMA, 0, 0)]))
        self.mm.enqueueDivision(Division([Player(PlayerType.ALPHA, 0, 0), Player(PlayerType.BETA, 0, 0),
                                          Player(PlayerType.GAMMA, 0, 0)]))

        successful = False
        bg = None
        while not successful:
            successful, bg = self.mm.processBattleGroups()

        self.assertTrue(successful)
        self.assertIsNotNone(bg)

        self.assertEqual(len(self.mm.queue), 0)

        self.assertEqual(len(bg.teams), self.params['teams_num'])

        for team in bg.teams:
            self.assertEqual(team.size, self.params['team_size'])
        for i, team in enumerate(bg.teams):
            for otherTeam in bg.teams[i:]:
                for playerType in list(PlayerType):
                    type_num = team.playersTypesNum[playerType]
                    other_type_num = otherTeam.playersTypesNum[playerType]
                    delta_type = abs(other_type_num - type_num)
                    max_type_diff = self.params['player_type_num_diff'][playerType]
                    self.assertLessEqual(delta_type, max_type_diff)


if __name__ == '__main__':
    unittest.main()
