"""\
Meshgrid goal explorer
"""
from __future__ import absolute_import, division, print_function
import random
import numbers
import collections

from .. import conduits
from .reuse import meshgrid
from . import m_rand


defcfg = m_rand.defcfg._copy(deep=True)
defcfg._describe('res', instanceof=(numbers.Integral, collections.Iterable),
                 docstring='resolution of the meshgrid')


class MeshgridMotorExplorer(m_rand.RandomMotorExplorer):
    """\
    Necessitate a sensory bounded environement.
    """
    defcfg = defcfg

    def __init__(self, cfg, **kwargs):
        super(MeshgridMotorExplorer, self).__init__(cfg)
        self._meshgrid = meshgrid.MeshGrid([c.bounds for c in self.m_channels], cfg.res)

    def _random_goal(self, bounds=None):
        if bounds is None:
            bounds = (c.bounds for c in self.m_channels)
        return collections.OrderedDict((c.name, c.fixed if c.fixed is not None else random.uniform(*b))
                                       for c, b in zip(self.m_channels, bounds))

    def explore(self):
        # pick a random bin
        if len(self._meshgrid._nonempty_bins) == 0:
            order = self._random_order()
        else:
            mbin = random.choice(self._meshgrid._nonempty_bins)
            if mbin.bounds is None:
                order = self._random_order()
            else:
                goal = self._random_order(mbin.bounds)

        return {'order': order, 'type': 'motorbabbling.mesh'}

    def receive(self, feedback):
        super(MeshgridMotorExplorer, self).receive(feedback)
        self._meshgrid.add(self._to_vector(feedback['order'], self.m_channels), feedback['feedback'])
