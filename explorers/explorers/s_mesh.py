"""\
Meshgrid goal explorer
"""
from __future__ import absolute_import, division, print_function
import random
import numbers
import collections

from .. import conduits
from .reuse import meshgrid
from . import s_rand


defcfg = s_rand.defcfg._copy(deep=True)
defcfg._describe('res', instanceof=(numbers.Integral, collections.Iterable),
                 docstring='resolution of the meshgrid')


class MeshgridGoalExplorer(s_rand.RandomGoalExplorer):
    """\
    Necessitate a sensory bounded environement.
    """
    defcfg = defcfg

    def __init__(self, cfg, inv_learners=(), **kwargs):
        super(MeshgridGoalExplorer, self).__init__(cfg, inv_learners=inv_learners)
        self._meshgrid = meshgrid.MeshGrid([c.bounds for c in self.s_channels], cfg.res)

    def _random_goal(self, bounds):
        return collections.OrderedDict((c.name, c.fixed if c.fixed is not None else random.uniform(*b))
                                       for c, b in zip(self.s_channels, bounds))

    def explore(self):
        # pick a random bin
        if len(self._meshgrid._nonempty_bins) == 0:
            goal = collections.OrderedDict((c.name, c.fixed if c.fixed is not None else random.uniform(*c.bounds))
                                            for c in self.s_channels)
        else:
            mbin = random.choice(self._meshgrid._nonempty_bins)
            if mbin.bounds is None:
                goal = collections.OrderedDict((c.name, c.fixed if c.fixed is not None else random.uniform(*c.bounds))
                                                for c in self.s_channels)
            else:
                goal = self._random_goal(mbin.bounds)

        order = self._inv_request(goal)
        return {'order': order, 'goal': goal, 'type': 'goalbabbling.mesh'}

    def receive(self, feedback):
        super(MeshgridGoalExplorer, self).receive(feedback)
        self._meshgrid.add(self._to_vector(feedback['feedback'], self.s_channels), feedback['order'])
