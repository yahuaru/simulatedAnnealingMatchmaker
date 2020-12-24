import unittest  # The test framework

from MatchmakerConditions import SHIP_TYPE_DIFFERENCE, TEAM_SIZE, TEAMS_NUM, Division
from player import Player, PlayerType
from simulatedAnnealing import SimulatedAnnealingMatchmaker


class Test_SimulatedAnnealingMatchmaker(unittest.TestCase):
    def setUp(self):
        self.mm = SimulatedAnnealingMatchmaker()
        self.mm.initProcess()

    def tearDown(self) -> None:
        self.mm.cleanup()

    def test_processBattleGroup(self):

        for i in range(TEAMS_NUM):
            player = Player(PlayerType.ALPHA, 0, 0)
            division = Division()
            division.addPlayer(player)
            self.mm.enqueueDivision(division)

        for i in range(TEAMS_NUM):
            player = Player(PlayerType.BETA, 0, 0)
            division = Division()
            division.addPlayer(player)
            self.mm.enqueueDivision(division)

        for i in range(TEAMS_NUM):
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

        for team in bg.teams:
            self.assertEqual(team.size, TEAM_SIZE)
        for i, team in enumerate(bg.teams):
            for otherTeam in bg.teams[i:]:
                for playerType in list(PlayerType):
                    type_num = team.playersTypesNum[playerType]
                    other_type_num = otherTeam.playersTypesNum[playerType]
                    delta_type = abs(other_type_num - type_num)
                    max_type_diff = SHIP_TYPE_DIFFERENCE[playerType]
                    self.assertLessEqual(delta_type, max_type_diff)


if __name__ == '__main__':
    unittest.main()
