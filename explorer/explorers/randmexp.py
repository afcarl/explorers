"""\
Pure random explorer.
Needs motor boundaries.
"""
from __future__ import absolute_import, division, print_function
import random
import collections

import forest

from .. import conduits

defcfg = forest.Tree()
defcfg._describe('m_channels', instanceof=collections.Iterable,
                 docstring='Motor channels to generate random order of')

class RandomMotorExplorer(object):
    """"""
    defcfg = defcfg

    def __init__(self, cfg):
        self.m_channels = cfg.m_channels
        self.obs_conduit = conduits.UnidirectionalHub()

    def explore(self):
        order = {c.name: random.uniform(*c.bounds) for c in self.m_channels}
        return {'order': order, 'type': 'motorbabbling'}

    def receive(self, feedback):
        self.obs_conduit.receive(feedback)


