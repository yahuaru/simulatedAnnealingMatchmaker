import csv
import random
import time
from threading import RLock

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
            'initial_temperature': 4,
        },
    'test_battle_group_1':
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
            'initial_temperature': 4,
        },
    'test_battle_group_2':
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
            'initial_temperature': 4,
        },
    'test_battle_group_3':
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
            'initial_temperature': 4,
        },
    'test_battle_group_4':
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
            'initial_temperature': 4,
        },
    'test_battle_group_5':
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
            'initial_temperature': 4,
        },
    'test_battle_group_6':
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
            'initial_temperature': 4,
        },
    'test_battle_group_7':
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
            'initial_temperature': 4,
        },
    'test_battle_group_8':
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
            'initial_temperature': 4,
        },

    'test_battle_group_9':
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
            'initial_temperature': 4,
        },

    'test_battle_group_10':
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
            'initial_temperature': 4,
        },

    'test_battle_group_11':
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
            'initial_temperature': 4,
        },
    'test_battle_group_12':
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
            'initial_temperature': 4,
        },

    'test_battle_group_13':
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
            'initial_temperature': 4,
        },
    'test_battle_group_14':
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
            'initial_temperature': 4,
        },

    'test_battle_group_15':
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
            'initial_temperature': 4,
        },
    'test_battle_group_16':
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
            'initial_temperature': 4,
        },

    'test_battle_group_17':
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
            'initial_temperature': 4,
        },
    }

divisions_num = 4000

if __name__ == '__main__':
    for process_num in range(1, 25):
        print("start_process", process_num)
        index = 0
        mm = MatchmakerProcessManager(process_num, params)
        for bt in params:
            for i in range(divisions_num):
                enqueue_time = random.random() * 100.0
                division = generate_division(index, 3, enqueue_time, 1, 8)
                index += 1
                mm.enqueue_division(bt, division)

        results = mm.start_process()
        print("finish_process", process_num)
        with open('data/process_collection_time_bt_{}.csv'.format(process_num), 'w', newline='') as tries_csv:
            tries_data_writer = csv.DictWriter(tries_csv, ["process", "result", "start_time", "finish_time"])
            tries_data_writer.writeheader()
            print(len(results))
            for i, result in enumerate(results):
                for iteration in result:
                    start_time, finish_time, result_code = iteration
                    tries_data_writer.writerow({"process": i, "result": result_code, "start_time": start_time, "finish_time": finish_time})
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
