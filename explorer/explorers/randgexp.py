"""\
Pure random sensory explorer.
Needs motor and sensor boundaries.
"""
from __future__ import absolute_import, division, print_function, unicode_literals
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
    """"""
    defcfg = defcfg

    def __init__(self, cfg, inv_learners = []):
        self.cfg = cfg
        self.cfg._update(defcfg)
        self.s_channels = {c.name:c for c in cfg.s_channels}
        self.m_channels = {c.name:c for c in cfg.m_channels}
        self.obs_conduit = conduits.UnidirectionalHub()
        self.inv_conduit = conduits.BidirectionalHub()
        for learner in inv_learners:
            self.inv_conduit.register(learner)

    def explore(self):
        self._goal  = {cname:random.uniform(*c.bounds) for cname, c in self.s_channels.items()}
        orders = self.inv_conduit.poll({'goal': self._goal,
                                        'm_channels': self.m_channels.values()})
        return random.choice(orders)

    def receive(self, feedback):
        self.obs_conduit.receive(feedback)
