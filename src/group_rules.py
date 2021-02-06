import bisect
from collections import namedtuple

from MatchmakerConditions import buildConditions


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


RuleState = namedtuple("SimulatedAnnealingParamsState", ["temperature", "conditions_param", "conditions", "actions"])