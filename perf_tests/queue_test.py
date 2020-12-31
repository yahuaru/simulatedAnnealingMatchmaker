import pickle
import time

import pandas as pd

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

try_name = "n6_ts6_log(1+x)"

params = {
    'teams_num': 6,
    'team_size': 6,
    'player_type_num_diff': {
        PlayerType.ALPHA: 1,
        PlayerType.BETA: 1,
        PlayerType.GAMMA: 1,
    },
    'initial_temperature': 9
}

logger = Logger()
mm = SimulatedAnnealingMatchmaker(params, logger)
# mm = SimulatedAnnealingMatchmaker()

f = open("divisions.dump", "rb")
players = pickle.load(f)

try_data = []

mm.startProcess()
mm.queue = list(players)

start_time = time.time()

process_time = 0

queue_process_time = time.time()

while mm.queue:
    bg = None

    mm.startProcess()

    successful = False
    while not successful:
        successful, bg = mm.processBattleGroups()

        process_time = time.time() - start_time
        if process_time > MAX_PROCESS_TIME:
            break

    if not successful:
        mm.stopProcess()

    start_time = time.time()
    print(successful, bg)
    print(len(mm.queue))


print(time.time() - queue_process_time)

mm.cleanup()
logger.cleanup()

df_iterations = pd.DataFrame([iteration[1:] for iteration in logger.iterations],
                             index=pd.MultiIndex.from_tuples([iteration[0] for iteration in logger.iterations],
                                                             names=["try_num", "iteration"]),
                             columns=["temperature", "energy", "probability"])
