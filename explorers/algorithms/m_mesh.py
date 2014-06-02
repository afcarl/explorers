"""\
Meshgrid goal explorer
"""
from __future__ import absolute_import, division, print_function
import random
import numbers
import collections

from .. import conduits
from .. import tools
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

    def explore(self):
        # pick a random bin
        if len(self._meshgrid._nonempty_bins) == 0:
            m_goal = tools.random_signal(self.m_channels)
        else:
            m_bin = random.choice(self._meshgrid._nonempty_bins)
            m_goal = tools.random_signal(self.m_channels, bounds=m_bin.bounds)

        return {'m_goal': m_goal, 'from': 'motor.babbling.mesh'}

    def receive(self, feedback):
        super(MeshgridMotorExplorer, self).receive(feedback)
        self._meshgrid.add(tools.to_vector(feedback['m_signal'], self.m_channels), feedback['s_signal'])
