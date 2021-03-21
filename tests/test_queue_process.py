from multiprocessing import Pipe

from battle_group.battle_group import BattleGroup
from multiprocess_mathmaker.queue_pipe import QueueManagerProxy
from multiprocess_mathmaker.queue_process import QueueManagerProcess
from rules_builder.rules_director import RulesDirector
from tests.helper_functions import generate_division


params = {
    'test':
        {
            'type': 'base',
            'teams_num': 3,
            'min_team_size': 3,
            'max_team_size': 3,
        }
    }


def test_enqueue():
    queue_key_builders = {}
    for battle_type, rules_battle_type in params.items():
        queue_key_builders[battle_type] = RulesDirector.build_queue_key_builder(rules_battle_type)

    queue_connectors = []
    queue_pipe, matchmaker_pipe = Pipe()
    queue_connectors.append(queue_pipe)
    queue_connector = QueueManagerProxy(matchmaker_pipe)
    queue_process = QueueManagerProcess(queue_key_builders, queue_connectors)
    queue_process.start()
    division = generate_division(0, 3)
    queue_connector.enqueue("test", division)
    result = queue_connector.pop("test", BattleGroup(), 3)
    assert result is not None
    assert result.id == division.id
    queue_process.terminate()
