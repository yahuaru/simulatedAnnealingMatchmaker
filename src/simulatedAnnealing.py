import bisect
from collections import namedtuple

from MatchmakerConditions import buildConditions
from matchmaker_queue.queue_manager import QueueManager
from simulatedAnnealingThread import SimulatedAnnealingMatchmakerThread


RuleState = namedtuple("SimulatedAnnealingParamsState", ["temperature", "conditions_param", "conditions", "actions"])


class BattleRules(object):
    def __init__(self, params):
        common_conditions_params = params['common_conditions']
        self._teams_num = common_conditions_params['teams_num']

        self._time = []
        self._states = []
        # sort params by time for ease of bisecting
        params_by_time = list(params['by_time'].items())
        params_by_time.sort(key=lambda param: param[0])
        for param_state_time, param in params_by_time:
            self._time.append(param_state_time)

            conditions_param = param['conditions'].copy()
            conditions_param.update(common_conditions_params)
            conditions, actions_classes = buildConditions(conditions_param)
            state = RuleState(param['initial_temperature'], conditions_param, conditions, actions_classes)
            self._states.append(state)

    def get_state_by_time(self, state_time):
        current_param_index = bisect.bisect(self._time, state_time) - 1
        return self._states[current_param_index]

    @property
    def teams_num(self):
        return self._teams_num


class MatchmakerThreadBuilder(object):
    def __init__(self, params):
        self.__param_by_battle_type = {}
        for battle_type, battle_type_params in params.items():
            self.__param_by_battle_type[battle_type] = BattleRules(params[battle_type])

    def build_thread(self, available_queue, on_thread_finished):
        thread_params = self.__param_by_battle_type[available_queue.battle_type]
        return SimulatedAnnealingMatchmakerThread(available_queue, thread_params, on_thread_finished)


class SimulatedAnnealingMatchmaker:
    def __init__(self, params, threads_num, on_battle_group_collected):
        self.__queue_manager = QueueManager(params)
        self.__thread_builder = MatchmakerThreadBuilder(params)

        self.__threads_num = threads_num
        self.__on_battle_group_collected = on_battle_group_collected

        self.__is_processing = False

        self.__threads = []

    def __on_thread_finished(self, thread, is_successful, battle_group):
        if is_successful:
            self.__on_battle_group_collected(battle_group)
        self.__threads.remove(thread)

    def startProcess(self):
        for i in range(len(self.__threads), self.__threads_num):
            queue_entry = self.__queue_manager.get_next_available_queue()
            if queue_entry is None:
                break
            thread = self.__thread_builder.build_thread(queue_entry, self.__on_thread_finished)
            self.__threads.append(thread)
            thread.startProcessing()

    def waitForCompletion(self):
        for thread in self.__threads:
            if thread.is_alive():
                thread.join()

    def stopProcess(self):
        for thread in self.__threads:
            if thread.is_alive():
                thread.stopProcessing()
                thread.join()

    def enqueueDivision(self, battle_type, division):
        self.__queue_manager.enqueue(battle_type, division)

    def dequeueDivision(self, battle_type, division):
        self.__queue_manager.dequeue(battle_type, division)

    @staticmethod
    def __getPenalty(battle_group, penalty_conditions):
        return sum(condition.check(battle_group) for condition in penalty_conditions)
