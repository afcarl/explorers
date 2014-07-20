"""\
Goal are chosen amongst a predefined set. Useful for tests.
"""
from __future__ import absolute_import, division, print_function
import random
import collections

import learners

from .. import explorer
from .. import tools
from .s_rand import RandomGoalExplorer


defcfg = RandomGoalExplorer.defcfg._copy(deep=True)
defcfg._describe('s_goals', instanceof=collections.Iterable,
                 docstring='Set of goals to choose from')
defcfg.classname = 'explorers.GoalSetExplorer'


class GoalSetExplorer(RandomGoalExplorer):
    """\
    Goal are chosen amongst a predefined set. Useful for tests.
    """
    defcfg = defcfg

    def __init__(self, cfg, **kwargs):
        super(GoalSetExplorer, self).__init__(cfg)
        self.s_goals = self.cfg.s_goals
        self.cursor = 0

    def explore(self):
        if self.cursor < len(self.s_goals):
            s_goal = self.s_goals[self.cursor]
            self.cursor += 1
            m_goal = self._inv_request(s_goal)
            if m_goal is None:
                m_goal = tools.avg_signal(self.m_channels)
            return {'m_goal': m_goal, 's_goal': s_goal, 'from': 'goal.babbling.set'}

    def _inv_request(self, s_goal):
        orders = self.inv_conduit.poll({'s_goal': s_goal,
                                        'm_channels': self.m_channels})
        return None if len(orders) == 0 else random.choice(orders)
