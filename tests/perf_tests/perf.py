import csv
import random
import time

from multiprocess_mathmaker.matcmaker import MatchmakerProcessManager
from player import PlayerType
from tests.helper_functions import generate_division

MAX_PROCESS_TIME = 0.7
MAX_TRIES = 1000

TEAMS_NUM = 4
TEAM_SIZE = 3

params = {
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

try_name = "n{}_ts{}_no_queue_split".format(TEAMS_NUM, TEAM_SIZE)

try_data = []



index = 0
# iterations_csv = open('data/iterations_data_{}.csv'.format(try_name), mode='w')
iterations_data_writer = None
# tries_csv = open('data/try_data_{}.csv'.format(try_name), mode='w')
# tries_data_writer = csv.DictWriter(tries_csv, ["final_iteration", "process_time"])
# tries_data_writer.writeheader()

if __name__ == '__main__':
    mm = MatchmakerProcessManager(1, params)
    failed_attempts = 0
    successful_attempts = 0


    mm.start_process()
    for j in range(40):
        divisions_num = 1000

        for i in range(divisions_num):
            enqueue_time = random.random() * 100.0
            division = generate_division(index, 3, enqueue_time, 1, 8)
            index += 1
            mm.enqueue_division("test_battle_group", division)
    while True:
        pass
#
# battle_group = mm.process()
# try_data = []
# divisions_left_num = divisions_num
# while divisions_left_num > TEAMS_NUM * TEAM_SIZE:
#     start_time = time.process_time_ns()
#     battle_group = mm.process()
#     process_time = time.process_time_ns() - start_time
#     print(battle_group)
#     divisions_left_num -= 12
#     print(j, divisions_left_num)
#     if battle_group is None:
#         failed_attempts += 1
#     else:
#         successful_attempts += 1
# print(failed_attempts, successful_attempts)
