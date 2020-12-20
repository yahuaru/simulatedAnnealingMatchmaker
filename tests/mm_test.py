import unittest  # The test framework

from MatchmakerConditions import SHIP_TYPE_DIFFERENCE, TEAM_SIZE
from player import Player, PlayerType
from simulatedAnnealing import SimulatedAnnealingMatchmaker


class Test_SimulatedAnnealingMatchmaker(unittest.TestCase):
    def setUp(self):
        self.mm = SimulatedAnnealingMatchmaker()

    def test_processBattleGroup(self):

        for i in range(3):
            player = Player(PlayerType.ALPHA, 0, 0)
            self.mm.enqueueDivision(player)

        for i in range(3):
            player = Player(PlayerType.BETA, 0, 0)
            self.mm.enqueueDivision(player)
            
        for i in range(3):
            player = Player(PlayerType.GAMMA, 0, 0)
            self.mm.enqueueDivision(player)
        

        successful = False
        bg = None
        while not successful:
            successful, bg = self.mm.proccessBattleGroups()
        
        self.assertTrue(successful)
        self.assertIsNotNone(bg)
        
        for team in bg.teams:
            self.assertEqual(team.size, TEAM_SIZE)
        for i, team in enumerate(bg.teams):
            for otherTeam in bg.teams[i:]:
                for playerType in list(PlayerType):
                    self.assertLessEqual(abs(otherTeam.playersTypesNum[playerType] - team.playersTypesNum[playerType]), SHIP_TYPE_DIFFERENCE[playerType])

if __name__ == '__main__':
    unittest.main()
