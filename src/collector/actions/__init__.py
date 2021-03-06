from random import shuffle

from .add_division import AddDivisionAction
from .add_teams import AddTeamsAction
from .remove_division import RemoveDivisionAction
from .remove_team import RemoveTeamAction
from .swap_division_from_queue import SwapDivisionsFromQueueAction
from .swap_divisions import SwapDivisionsAction

PRIORITY_ACTIONS = (AddTeamsAction, RemoveTeamAction)
ACTIONS = (AddDivisionAction, RemoveDivisionAction, SwapDivisionsFromQueueAction, SwapDivisionsAction)


def random_actions_generator(rules):
    for action_class in PRIORITY_ACTIONS:
        yield action_class(rules)

    actions = list(ACTIONS)
    shuffle(actions)
    for action_class in actions:
        yield action_class(rules)
