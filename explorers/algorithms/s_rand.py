"""\
Pure random sensory explorer.
Needs motor and sensor boundaries.
"""
from __future__ import absolute_import, division, print_function
import random
import collections

import forest
import learners

from .. import conduits
from .. import explorer
from .. import tools


defcfg = explorer.defcfg._copy(deep=True)
defcfg._describe('s_channels', instanceof=collections.Iterable,
                 docstring='Sensory channels to generate random goal from')
defcfg._branch('learner')

class RandomGoalExplorer(explorer.Explorer):
    """\
    Just a random explorer
    Necessitate a sensory bounded environement.
    """
    defcfg = defcfg

    def __init__(self, cfg, inv_learners=(), **kwargs):
        super(RandomGoalExplorer, self).__init__(cfg)
        self.s_channels = cfg.s_channels
        self.inv_conduit = conduits.BidirectionalHub()

        if len(self.cfg.learner) > 0:
            self.cfg.learner.m_channels = self.m_channels
            self.cfg.learner.s_channels = self.s_channels
            learner = learners.Learner.create(self.cfg.learner)
            inv_learners = (learner,) + tuple(inv_learners)
        for learner in inv_learners:
            self.inv_conduit.register(learner.inv_request)
            self.obs_conduit.register(learner.update_request)

    def explore(self):
        s_goal = tools.random_signal(self.s_channels)
        m_goal = self._inv_request(s_goal)
        if m_goal is None:
            m_goal = tools.random_signal(self.m_channels)
        return {'m_goal': m_goal, 's_goal': s_goal, 'from': 'goal.babbling'}

    def _inv_request(self, s_goal):
        orders = self.inv_conduit.poll({'s_goal': s_goal,
                                        'm_channels': self.m_channels})
        return None if len(orders) == 0 else random.choice(orders)

