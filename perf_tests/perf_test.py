import csv
import random
import time


from player import PlayerType
from simple_matchmaker import SimpleMatchmaker
from stat_logging import stat_logging
from tests.helper_functions import generateDivision
from timeit import default_timer as timer

MAX_PROCESS_TIME = 0.7
MAX_TRIES = 1000

TEAMS_NUM = 4
TEAM_SIZE = 3

T_0 = 4

params = {
    'test_battle_group':
        {
            'common_conditions': {
                'teams_num': TEAMS_NUM,
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
                    'initial_temperature': T_0,
                },
            }
        }
}

try_name = "n{}_ts{}_t{}_average_ruleset_refactored_queue".format(TEAMS_NUM, TEAM_SIZE, T_0)

try_data = []

failed_attempts = 0
mm = SimpleMatchmaker(params)

iterations_csv = open('data/iterations_data_{}.csv'.format(try_name), mode='w')
iterations_data_writer = None
tries_csv = open('data/try_data_{}.csv'.format(try_name), mode='w')
tries_data_writer = csv.DictWriter(tries_csv, ["try_index", "final_iteration", "process_time"])
tries_data_writer.writeheader()

group_csv = open('data/groups_data_{}.csv'.format(try_name), mode='w')
group_data_writer = csv.DictWriter(group_csv, ['try_index', 'division_id', 'team_id', 'number', 'enqueue_time'])
group_data_writer.writeheader()

division_index = 0
try_index = 0
iteration_row_index = 0
fails = 0
for j in range(40):
    divisions_num = 1000

    for i in range(divisions_num):
        enqueue_time = random.randint(0, 1000)
        division = generateDivision(division_index, 3, enqueue_time, 1, 8)
        division_index += 1
        mm.enqueueDivision("test_battle_group", division)

    battle_group = mm.process()
    try_data = []
    divisions_left_num = divisions_num
    group_number = 0
    while divisions_left_num > TEAMS_NUM * TEAM_SIZE:
        start_time = time.perf_counter_ns()
        battle_group = mm.process()
        print(battle_group)
        process_time = time.perf_counter_ns() - start_time
        divisions_left_num -= 12
        print(j, divisions_left_num)
        if battle_group is not None:
            for team_id, team in enumerate(battle_group.teams):
                for division in team.divisions:
                    group_data_writer.writerow({
                        'try_index': try_index,
                        'division_id': division.id,
                        'team_id': team_id,
                        'number': group_number,
                        'enqueue_time': division.enqueue_time,
                    })
            group_number += 1
            tries_data_writer.writerow(
                {
                    'try_index': try_index,
                    'final_iteration': stat_logging.iterations[-1]['iteration'],
                    "process_time": process_time}
            )
            if iterations_data_writer is None:
                iterations_data_writer = csv.DictWriter(iterations_csv, ["row_index", "try_index"] + list(stat_logging.iterations[-1].keys()))
                iterations_data_writer.writeheader()
            for iteration_data in stat_logging.iterations:
                iteration_data["try_index"] = try_index
                iteration_data["row_index"] = iteration_row_index
                iteration_row_index += 1
                iterations_data_writer.writerow(iteration_data)
            try_index += 1
            stat_logging.cleanup()
        else:
            fails += 1

print("Fails:", fails, try_index)