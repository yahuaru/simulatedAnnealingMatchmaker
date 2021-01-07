import copy
import time
from collections import namedtuple

from MatchmakerConditions import buildConditions
from simulatedAnnealingQueue import SimulatedAnnealingMatchmakerQueue
from simulatedAnnealingThread import SimulatedAnnealingMatchmakerThread

THREADS_NUM = 1


ParamsState = namedtuple("SimulatedAnnealingParamsState", ["temperature", "conditions", "actions"])


class SimulatedAnnealingMatchmaker:
    def __init__(self, params, on_battle_group_collected, queue=None):
        self.__queue = SimulatedAnnealingMatchmakerQueue(queue)

        self.__on_battle_group_collected = on_battle_group_collected

        self.__teams_num = params['teams_num']

        self.__is_processing = False

        self.__param_state_by_time = {'time': [], 'states': []}
        common_params = copy.deepcopy(params)
        params_by_time = list(common_params.pop('by_time').items())
        params_by_time.sort(key=lambda param: param[0])
        for param_time, param in params_by_time:
            self.__param_state_by_time['time'].append(param_time)

            param.update(common_params)
            conditions, actions = buildConditions(param)
            state = ParamsState(param['initial_temperature'], conditions, actions)
            self.__param_state_by_time['states'].append(state)

        self.__threads = []
        for i in range(THREADS_NUM):
            thread = SimulatedAnnealingMatchmakerThread(self.__queue, self.__param_state_by_time, self.__onThreadFinished)
            self.__threads.append(thread)

    def __onThreadFinished(self, thread, is_successful, battle_group):
        if not is_successful:
            if self.__is_processing:
                current_time = time.time()
                thread.prepareProcessing(current_time)
            else:
                thread.stopProcessing()
        else:
            self.__on_battle_group_collected(battle_group)

    def clear(self):
        self.__queue.clear()
        self.__param_state_by_time.clear()

    def startProcess(self):
        self.__is_processing = True
        for thread in self.__threads:
            thread.prepareProcessing(self.__teams_num)
            thread.start()

    def waitForCompletion(self):
        for thread in self.__threads:
            if thread.is_active:
                thread.join()

    def stopProcess(self):
        self.__is_processing = False
        for thread in self.__threads:
            thread.stopProcessing()
            thread.join()

    def enqueueDivision(self, division):
        self.__queue.pushDivision(division)

    def dequeueDivision(self, division):
        self.__queue.removeDivision(division)

    @staticmethod
    def __getPenalty(battle_group, penalty_conditions):
        return sum(condition.check(battle_group) for condition in penalty_conditions)
