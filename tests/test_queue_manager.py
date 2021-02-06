import pytest

from battleGroup import Division
from player import Player, PlayerType
from queue_manager import QueueManager

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
    index = 0
    for level in range(1, 7):
        for i in range(10):
            division = Division(index)
            for j in range(3):
                player = Player(PlayerType.ALPHA, level)
                division.addPlayer(player)
            index += 1
            queue_manager.enqueue('test', division)

    # check we have right queues
    resulted_queues = [('test', 2), ('test', 3), ('test', 4), ('test', 5), ('test', 6), ('test', 7)]

    key_queue = queue_manager.get_next_available_queue()
    while key_queue:
        queue_manager_entry = key_queue
        assert queue_manager_entry.key in resulted_queues
        resulted_queues.remove(queue_manager_entry.key)

        queue = queue_manager_entry.queue
        # check that level difference satisfy rules
        division = queue_manager_entry.queue.pop()
        assert division is not None
        min_level = division.max_level
        max_level = division.max_level
        max_level_difference = params['test']['common_conditions']['by_level']['max_level_difference']
        while queue:
            division = queue.pop()
            assert division is not None
            assert abs(division.max_level - max_level) <= max_level_difference
            assert abs(division.max_level - min_level) <= max_level_difference
            max_level = max(division.max_level, max_level)
            min_level = min(division.max_level, min_level)

        key_queue = queue_manager.get_next_available_queue()
