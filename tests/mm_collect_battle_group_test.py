import unittest

from battle_group.division import Division
from player import Player, PlayerType
from simple_matchmaker import SimpleMatchmaker

TEAMS_NUM = 3
TEAM_SIZE = 3


class Test_CollectBattleGroup(unittest.TestCase):
    def setUp(self) -> None:
        self.params = {
            'test_battle_group':
                {
                    'type': 'base',
                    'teams_num': TEAMS_NUM,
                    'min_team_size': TEAM_SIZE,
                    'max_team_size': TEAM_SIZE,
                    'player_type_num_diff': {
                        PlayerType.ALPHA: 0,
                        PlayerType.BETA: 0,
                        PlayerType.GAMMA: 0,
                    },
                    'initial_temperature': 3,
                }
        }
        self.mm = SimpleMatchmaker(self.params)

    # T: D(ALPHA), D(BETA), D(GAMMA)
    # T: D(ALPHA), D(BETA), D(GAMMA)
    # T: D(ALPHA), D(BETA), D(GAMMA)
    def test_processBattleGroup(self):
        index = 0
        divisions = []
        for i in range(TEAMS_NUM):
            player = Player(PlayerType.ALPHA, 0)
            index += 1
            division = Division(index)
            division.add_player(player)
            self.mm.enqueue_division("test_battle_group", division)
            divisions.append(division)

        for i in range(TEAMS_NUM):
            player = Player(PlayerType.BETA, 0)
            index += 1
            division = Division(index)
            division.add_player(player)
            self.mm.enqueue_division("test_battle_group", division)
            divisions.append(division)

        for i in range(TEAMS_NUM):
            player = Player(PlayerType.GAMMA, 0)
            index += 1
            division = Division(index)
            division.add_player(player)
            self.mm.enqueue_division("test_battle_group", division)
            divisions.append(division)

        battle_group = self.mm.process()
        self.assertIsNotNone(battle_group)

        self.assertEqual(TEAMS_NUM, len(battle_group.teams))

        for team in battle_group.teams:
            self.assertEqual(TEAM_SIZE, team.size)
            for division in team.divisions:
                assert division in divisions
                divisions.remove(division)

        for i, team in enumerate(battle_group.teams):
            for otherTeam in battle_group.teams[i:]:
                for playerType in PlayerType:
                    type_num = team.players_types_num[playerType]
                    other_type_num = otherTeam.players_types_num[playerType]
                    delta_type = abs(other_type_num - type_num)
                    max_type_diff = \
                    self.params['test_battle_group']['player_type_num_diff'][playerType]
                    self.assertLessEqual(delta_type, max_type_diff)

    # T: D(GAMMA, BETA), D(ALPHA)
    # T: D(BETA, ALPHA), D(GAMMA)
    # T: D(ALPHA, BETA, GAMMA)
    def test_processDifferentSizeDivisionsBattleGroup(self):
        divisions = [
            Division(0, [Player(PlayerType.GAMMA, 0), Player(PlayerType.BETA, 0)]),
            Division(1, [Player(PlayerType.ALPHA, 0)]),
            Division(2, [Player(PlayerType.BETA, 0), Player(PlayerType.ALPHA, 0)]),
            Division(3, [Player(PlayerType.GAMMA, 0)]),
            Division(4, [Player(PlayerType.ALPHA, 0), Player(PlayerType.BETA, 0),
                         Player(PlayerType.GAMMA, 0)]),
        ]
        for division in divisions:
            self.mm.enqueue_division('test_battle_group', division)

        battle_group = self.mm.process()
        self.assertIsNotNone(battle_group)

        self.assertEqual(len(battle_group.teams), TEAMS_NUM)

        for team in battle_group.teams:
            self.assertEqual(team.size, TEAM_SIZE)
            for division in team.divisions:
                assert division in divisions
                divisions.remove(division)
        for i, team in enumerate(battle_group.teams):
            for otherTeam in battle_group.teams[i:]:
                for playerType in PlayerType:
                    type_num = team.players_types_num[playerType]
                    other_type_num = otherTeam.players_types_num[playerType]
                    delta_type = abs(other_type_num - type_num)
                    max_type_diff = \
                    self.params['test_battle_group']['player_type_num_diff'][playerType]
                    self.assertLessEqual(delta_type, max_type_diff)


if __name__ == '__main__':
    unittest.main()
