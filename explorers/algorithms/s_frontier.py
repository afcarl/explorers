"""\
Meshgrid goal explorer
"""
from __future__ import absolute_import, division, print_function
import random
import numbers
import collections

from .. import conduits
from .. import tools
from .. import meshgrid
from . import s_mesh


defcfg = s_mesh.MeshgridGoalExplorer.defcfg._copy(deep=True)
defcfg._pop('cutoff')
defcfg.classname = 'explorers.FrontierGoalExplorer'


class FrontierGoalExplorer(s_mesh.MeshgridGoalExplorer):
    """\
    Necessitate a sensory bounded environement.
    """
    defcfg = defcfg

    def _choose_goal(self):
        s_bins = self._meshgrid._nonempty_bins
        if len(s_bins) == 0:
            return None #s_goal = tools.random_signal(self.s_channels)
        else:
            s_bin = random.choice(s_bins)
            coo = s_bin.coo
            dim       = random.randint(0, len(coo)-1)
            direction = random.choice([-1, 1])
            s_goal = None
            while s_goal is None:
                coo = list(coo)
                coo[dim] += direction
                coo = tuple(coo)
                if coo not in self._meshgrid._bins:
                    s_bounds = self._meshgrid._bounds(coo)
                    s_goal   = tools.random_signal(self.s_channels, s_bounds)
            return s_goal

    def _explore(self):
        # pick a random bin
        s_goal   = self._choose_goal()
        m_signal = self._inv_request(s_goal)
        return {'m_signal': m_signal, 's_goal': s_goal, 'from': 'goal.babbling.unreach'}
