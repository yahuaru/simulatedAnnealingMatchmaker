import pytest

from battle_group import Division
from matchmaker_queue.key.queue_key_builder import QueueGroupKey
from player import Player, PlayerType
from matchmaker_queue.queue_manager import QueueManager

params = {
    'test':
        {
            'common_conditions': {
                'teams_num': 4,
                'by_level': {
                    'max_level_difference': 1,
                    'min_level': 1,
                    'max_level': 8,
                }
            },
            'by_time': {
                0: {
                    'max_team_size': 4,
                    'min_team_size': 1,
                    'divisions_allowed': True,
                }
            }
        }
}


@pytest.fixture
def queue_manager():
    return QueueManager(params)


def test_queue_manager(queue_manager):
    assert queue_manager


def test_get_next_available_queue(queue_manager):
    max_division_size = 3
    index = 0
    divisions = []
    for level in range(1, 7):
        for i in range(10):
            division = Division(index)
            for j in range(max_division_size):
                player = Player(PlayerType.ALPHA, level)
                division.add_player(player)
            divisions.append(division)
            index += 1
            queue_manager.enqueue('test', division)

    # check we have right queues
    resulted_queues = [QueueGroupKey('test', (2,)), QueueGroupKey('test', (3,)), QueueGroupKey('test', (4,)),
                       QueueGroupKey('test', (5,)), QueueGroupKey('test', (6,)), QueueGroupKey('test', (7,))]

    group_key = queue_manager.get_next_available_group_key()
    while group_key:
        assert group_key in resulted_queues
        resulted_queues.remove(group_key)

        # check that level difference satisfy rules
        division = queue_manager.pop(group_key, max_division_size)
        while division is not None:
            divisions.remove(division)
            min_level = division.max_level
            max_level = division.max_level
            max_level_difference = params['test']['common_conditions']['by_level']['max_level_difference']
            assert abs(division.max_level - max_level) <= max_level_difference
            assert abs(division.max_level - min_level) <= max_level_difference
            division = queue_manager.pop(group_key, max_division_size)
        group_key = queue_manager.get_next_available_group_key()

    assert 0 == len(divisions)
