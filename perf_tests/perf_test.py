import pickle
import time

import numpy as np
import pandas as pd

from MatchmakerConditions import buildConditions
from battleGroup import Team, BattleGroup
from player import PlayerType
from simulatedAnnealing import SimulatedAnnealingMatchmaker, SimulatedAnnealingMatchmakerLogger


class Logger(SimulatedAnnealingMatchmakerLogger):
    def __init__(self):
        super().__init__()
        self.iterations = []
        self.try_num = 0

    def cleanup(self):
        pass

    def logIteration(self, iteration, temperature, energy, prob):
        self.iterations.append([(self.try_num, iteration), temperature, energy, prob])


MAX_PROCESS_TIME = 0.7
MAX_TRIES = 1000

TEAMS_NUM = 4
TEAM_SIZE = 3

params = {
    'teams_num': TEAMS_NUM,
    'by_time': {
        0: {
            'max_team_size': TEAM_SIZE,
            'min_team_size': TEAM_SIZE,
            'player_type_num_diff': {
                PlayerType.ALPHA: 0,
                PlayerType.BETA: 0,
                PlayerType.GAMMA: 0,
            },
            'initial_temperature': 12
        }
    }
}

conditions, _ = buildConditions(params)
teams = [Team() for _ in range(params["teams_num"])]
current_battle_group = BattleGroup(teams)
print(sum(condition.check(current_battle_group) for condition in conditions))


try_name = "n{}_ts{}".format(TEAMS_NUM, TEAM_SIZE)

logger = Logger()

f = open("divisions.dump", "rb")
players = pickle.load(f)

try_data = []

failed_attempts = 0
for i in range(MAX_TRIES):
    mm = SimulatedAnnealingMatchmaker(params, players, logger)

    mm.startProcess()

    start_time = time.time()

    logger.try_num = i

    successful = False
    process_time = 0
    while not successful:
        successful, bg = mm.processBattleGroups(0)

        process_time = time.time() - start_time
        if process_time > MAX_PROCESS_TIME:
            failed_attempts += 1
            break

    try_data.append([successful, mm.currentIteration, process_time])

    print("{:.0%} failed:{:.0%}".format(i / MAX_TRIES, failed_attempts/MAX_TRIES))

    mm.clear()
    logger.cleanup()

df_iterations = pd.DataFrame([iteration[1:] for iteration in logger.iterations],
                             index=pd.MultiIndex.from_tuples([iteration[0] for iteration in logger.iterations],
                                                             names=["try_num", "iteration"]),
                             columns=["temperature", "energy", "probability"])
df_try = pd.DataFrame(try_data, columns=["successful", "final_iteration", "process_time"])


df_iterations.to_csv('data/iterations_data_{}.csv'.format(try_name), )
df_try.to_csv('data/try_data_{}.csv'.format(try_name))

print(sorted(zip(*np.unique(df_iterations.energy, return_counts=True)), key=lambda v: v[1], reverse=True))