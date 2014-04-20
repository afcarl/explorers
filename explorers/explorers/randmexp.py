"""\
Pure random explorer.
Needs motor boundaries.
"""
from __future__ import absolute_import, division, print_function
import random
import collections

from . import explorer

class RandomMotorExplorer(explorer.Explorer):
    """"""

    def explore(self):
        order = collections.OrderedDict((c.name, random.uniform(*c.bounds)) for c in self.m_channels)
        return {'order': order, 'type': 'motorbabbling'}
