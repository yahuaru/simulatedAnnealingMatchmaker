from collector.rules.rules_collection import RulesState, IRulesCollection


class BaseRulesCollection(IRulesCollection):
    def __init__(self, rules, initial_temperature, conditions):
        self._rules = rules
        self._initial_temperature = initial_temperature
        self._conditions = conditions

    def get_state(self, battle_group):
        penalty = sum(condition.check(battle_group) for condition in self._conditions)
        return RulesState(self._initial_temperature, penalty, self._rules)
