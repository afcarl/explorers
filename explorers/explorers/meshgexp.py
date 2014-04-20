"""\
Meshgrid goal explorer
"""
from __future__ import absolute_import, division, print_function
import random
import numbers
import collections

from .. import conduits
from .reuse import meshgrid
from . import randgexp


defcfg = randgexp.defcfg._copy(deep=True)
defcfg._describe('res', instanceof=(numbers.Integral, collections.Iterable),
                 docstring='resolution of the meshgrid')


class MeshgridGoalExplorer(randgexp.RandomGoalExplorer):
    """\
    Necessitate a sensory bounded environement.
    """
    defcfg = defcfg

    def __init__(self, cfg, inv_learners=()):
        super(MeshgridGoalExplorer, self).__init__(cfg, inv_learners=inv_learners)
        self._meshgrid = meshgrid.MeshGrid([c.bounds for c in self.s_channels], cfg.res)

    def _random_goal(self, bounds):
        return collections.OrderedDict((c.name, c.fixed if c.fixed is not None else random.uniform(*b))
                                       for c, b in zip(self.s_channels, bounds))

    def explore(self):
        # pick a random bin
        if len(self._meshgrid._bins) == 1:
            goal = collections.OrderedDict((c.name, c.fixed if c.fixed is not None else random.uniform(*c.bounds))
                               for c in self.s_channels)
        else:
            mbin = random.choice(self._meshgrid._bins)
            if mbin.bounds is None:
                goal = collections.OrderedDict((c.name, c.fixed if c.fixed is not None else random.uniform(*c.bounds))
                                               for c in self.s_channels)
            else:
                goal = self._random_goal(mbin.bounds)

        orders = self.inv_conduit.poll({'goal': goal,
                                        'm_channels': self.m_channels})
        order = random.choice(orders)
        return {'order': order, 'goal': goal, 'type': 'goalbabbling.mesh'}
