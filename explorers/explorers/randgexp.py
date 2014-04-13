"""\
Pure random sensory explorer.
Needs motor and sensor boundaries.
"""
from __future__ import absolute_import, division, print_function
import random
import collections

import forest

from .. import conduits


defcfg = forest.Tree()
defcfg._describe('m_channels', instanceof=collections.Iterable,
                 docstring='Motor channels to generate random order of')
defcfg._describe('s_channels', instanceof=collections.Iterable,
                 docstring='Sensory channels to generate random goal from')

class RandomGoalExplorer(object):
    """\
    Just a random explorer
    Necessitate a sensory bounded environement.
    """
    defcfg = defcfg

    def __init__(self, cfg, inv_learners=()):
        self.cfg = cfg
        self.cfg._update(defcfg)
        self.s_channels = cfg.s_channels
        self.m_channels = cfg.m_channels
        self.obs_conduit = conduits.UnidirectionalHub()
        self.inv_conduit = conduits.BidirectionalHub()
        for learner in inv_learners:
            self.inv_conduit.register(learner.infer)
            self.obs_conduit.register(learner.update)
        self.goal = None

    def explore(self):
        self.goal  = collections.OrderedDict((c.name, random.uniform(*c.bounds)) for c in self.s_channels)
        orders = self.inv_conduit.poll({'goal': self.goal,
                                        'm_channels': self.m_channels})
        order = random.choice(orders)
        return {'order': order, 'goal': self.goal, 'type': 'goalbabbling'}

    def receive(self, feedback):
        self.obs_conduit.receive(feedback)
