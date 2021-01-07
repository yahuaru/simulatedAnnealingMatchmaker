import copy
import time
from collections import namedtuple

from MatchmakerConditions import buildConditions
from simulatedAnnealingQueue import SimulatedAnnealingMatchmakerQueue
from simulatedAnnealingThread import SimulatedAnnealingMatchmakerThread


ParamsState = namedtuple("SimulatedAnnealingParamsState", ["temperature", "conditions_param", "conditions", "actions"])


class SimulatedAnnealingMatchmaker:
    def __init__(self, params, threads_num, on_battle_group_collected, queue=None):
        self.__queue = SimulatedAnnealingMatchmakerQueue(queue)

        self.__threads_num = threads_num
        self.__on_battle_group_collected = on_battle_group_collected

        self.__teams_num = params['common_conditions']['teams_num']

        self.__is_processing = False

        self.__param_state_by_time = {'time': [], 'states': []}
        common_conditions_params = params['common_conditions']
        params_by_time = list(params['by_time'].items())
        params_by_time.sort(key=lambda param: param[0])
        for param_time, param in params_by_time:
            self.__param_state_by_time['time'].append(param_time)

            conditions_param = param['conditions'].copy()
            conditions_param.update(common_conditions_params)
            conditions, actions_classes = buildConditions(conditions_param)
            state = ParamsState(param['initial_temperature'], conditions_param, conditions, actions_classes)
            self.__param_state_by_time['states'].append(state)

        self.__threads = []

    def __onThreadFinished(self, thread, is_successful, battle_group):
        if is_successful:
            self.__on_battle_group_collected(battle_group)
        self.__threads.remove(thread)

    def clear(self):
        self.stopProcess()

        self.__queue.clear()
        self.__param_state_by_time.clear()

    def startProcess(self):
        for i in range(len(self.__threads), self.__threads_num):
            thread = SimulatedAnnealingMatchmakerThread(self.__queue, self.__param_state_by_time, self.__onThreadFinished)
            self.__threads.append(thread)

            thread.startProcessing(self.__teams_num)

    def waitForCompletion(self):
        for thread in self.__threads:
            if thread.is_alive():
                thread.join()

    def stopProcess(self):
        for thread in self.__threads:
            if thread.is_alive():
                thread.stopProcessing()
                thread.join()

    def enqueueDivision(self, division):
        self.__queue.pushDivision(division)

    def dequeueDivision(self, division):
        self.__queue.removeDivision(division)

    @staticmethod
    def __getPenalty(battle_group, penalty_conditions):
        return sum(condition.check(battle_group) for condition in penalty_conditions)
