import unittest  # The test framework
from unittest.mock import patch

from battle_group import Division
from player import Player, PlayerType
from simple_matchmaker import SimpleMatchmaker

TEAMS_NUM = 3
MAX_TEAM_SIZE = 3
MIN_TEAM_SIZE = 2

SECOND_TRY_TIME = 20


class Test_SimulatedAnnealingMatchmaker(unittest.TestCase):
    def setUp(self) -> None:
        self.params = {
            'test_battle_group': {
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
        }
        self.mm = SimpleMatchmaker(self.params)

    # T: D(ALPHA), D(BETA), D(GAMMA)
    # T: D(ALPHA), D(BETA), D(GAMMA)
    # T: D(ALPHA), D(BETA), D(GAMMA)
    @patch("time.time", return_value=0)
    def test_waitTimeConditions(self, time_patch):
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

        battle_group = self.mm.process()

        self.assertIsNotNone(battle_group)

        for team in battle_group.teams:
            for division in team.divisions:
                assert division in divisions
                divisions.remove(division)

        self.assertEqual(TEAMS_NUM, len(battle_group.teams))

        for team in battle_group.teams:
            self.assertEqual(team.size, MAX_TEAM_SIZE)
        for i, team in enumerate(battle_group.teams):
            for otherTeam in battle_group.teams[i:]:
                for playerType in list(PlayerType):
                    type_num = team.players_types_num[playerType]
                    other_type_num = otherTeam.players_types_num[playerType]
                    delta_type = abs(other_type_num - type_num)
                    max_type_diff = self.params['test_battle_group']['by_time'][0]['conditions']['player_type_num_diff'][playerType]
                    self.assertLessEqual(delta_type, max_type_diff)

        time_patch.return_value = SECOND_TRY_TIME
        battle_group = self.mm.process()

        self.assertIsNotNone(battle_group)

        self.assertEqual(len(battle_group.teams), TEAMS_NUM)

        for team in battle_group.teams:
            self.assertLessEqual(team.size, MAX_TEAM_SIZE)
            self.assertGreaterEqual(team.size, MIN_TEAM_SIZE)


if __name__ == '__main__':
    unittest.main()
