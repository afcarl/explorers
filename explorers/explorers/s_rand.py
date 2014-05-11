"""\
Pure random sensory explorer.
Needs motor and sensor boundaries.
"""
from __future__ import absolute_import, division, print_function
import random
import collections

import forest

from .. import conduits
from . import explorer
from .. import learners


defcfg = explorer.defcfg._copy(deep=True)
defcfg._describe('s_channels', instanceof=collections.Iterable,
                 docstring='Sensory channels to generate random goal from')

class RandomGoalExplorer(explorer.Explorer):
    """\
    Just a random explorer
    Necessitate a sensory bounded environement.
    """
    defcfg = defcfg

    def __init__(self, cfg, inv_learners=(), **kwargs):
        super(RandomGoalExplorer, self).__init__(cfg)
        self.cfg._update(defcfg, overwrite=False)
        self.s_channels = cfg.s_channels
        self.inv_conduit = conduits.BidirectionalHub()

        if 'learner' in self.cfg:
            learner = learners.ModelLearner(self.cfg.learner)
            inv_learners = (learner,) + tuple(inv_learners)
        for learner in inv_learners:
            self.inv_conduit.register(learner.infer)
            self.obs_conduit.register(learner.update)

    def explore(self):
        goal  = collections.OrderedDict((c.name, c.fixed if c.fixed is not None else random.uniform(*c.bounds)) for c in self.s_channels)
        order = self._inv_request(goal)
        return {'order': order, 'goal': goal, 'type': 'goalbabbling'}

    def _inv_request(self, goal):
        orders = self.inv_conduit.poll({'goal': goal,
                                        'm_channels': self.m_channels})
        return None if len(orders) == 0 else random.choice(orders)

