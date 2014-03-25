"""\
Pure random explorer.
Needs motor boundaries.
"""
from __future__ import absolute_import, division, print_function, unicode_literals
import random
import collections

import forest

from .. import conduits

defcfg = forest.Tree()
defcfg._describe('m_channels', instanceof=collections.Iterable,
                 docstring='Motor channels to generate random order of')

class RandomExplorer(object):
    """"""
    defcfg = defcfg

    def __init__(self, cfg):
        self.m_channels = cfg.m_channels
        self.obs_conduit = conduits.Hub()

    def explore(self):
        self._order = {c.name: random.uniform(*c.bounds) for c in self.m_channels}
        return self._order

    def receive(self, feedback):
        self.obs_conduit.receive({'order': self._order,
                                  'feedback': feedback})


