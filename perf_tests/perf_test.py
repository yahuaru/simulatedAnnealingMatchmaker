import csv
import random
import time

from greedy_strict_matchmaker import GreedyMatchmaker
from player import PlayerType
from tests.helper_functions import generateDivision

MAX_PROCESS_TIME = 0.7
MAX_TRIES = 1000

TEAMS_NUM = 4
TEAM_SIZE = 3

params = {
    'test_battle_group':
        {
            'common_conditions': {
                'teams_num': TEAMS_NUM,
                'by_level': {
                    'max_level_difference': 1,
                    'min_level': 1,
                    'max_level': 8,
                }
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
            }
        }
}

try_name = "n{}_ts{}_greedy_average_rules".format(TEAMS_NUM, TEAM_SIZE)

try_data = []

failed_attempts = 0
mm = GreedyMatchmaker(TEAM_SIZE, TEAMS_NUM)

index = 0
# iterations_csv = open('data/iterations_data_{}.csv'.format(try_name), mode='w')
# iterations_data_writer = None
tries_csv = open('data/try_data_{}.csv'.format(try_name), mode='w')
tries_data_writer = csv.DictWriter(tries_csv, ["process_time"])
tries_data_writer.writeheader()

tries = 0
failed = 0
for j in range(40):
    divisions_num = 1000

    for i in range(divisions_num):
        enqueue_time = random.random() * 100.0
        division = generateDivision(index, 3, enqueue_time, 1, 8)
        index += 1
        mm.enqueueDivision(division)

    battle_group = mm.process()
    try_data = []
    divisions_left_num = divisions_num
    while divisions_left_num > TEAMS_NUM * TEAM_SIZE:
        start_time = time.perf_counter_ns()
        battle_group = mm.process()
        print(battle_group)
        process_time = time.perf_counter_ns() - start_time
        divisions_left_num -= 12
        print(j, divisions_left_num)
        if battle_group is not None:
            tries += 1
            tries_data_writer.writerow(
                {"process_time": process_time}
            )
        else:
            failed += 1

print(tries, failed)