"""Reuse generators, that yield order to reuse"""

from __future__ import print_function, division, absolute_import
import random
import numbers

import forest

from . import s_reusegen
from ..m_rand import RandomMotorExplorer


algorithms = {'random'        : s_reusegen.RandomReuse,
              'sensor_uniform': s_reusegen.SensorUniformReuse}

defcfg = forest.Tree(strict=True)
defcfg._update(RandomMotorExplorer.defcfg)
defcfg._describe('reuse.algorithm', instanceof=str,
                 docstring='name of the reuse algorithm to use')
defcfg._describe('reuse.discount', instanceof=numbers.Real, default=1.0,
                 docstring='how much the ratio decrease with each reuse')
defcfg.classname = 'explorers.ReuseExplorer'


for algorithm in algorithms.values():
    defcfg._update(algorithm.defcfg)


class ReuseExplorer(RandomMotorExplorer):
    """A reuse explorer"""

    defcfg = defcfg

    def __init__(self, cfg, dataset=None, **kwargs):
        super(ReuseExplorer, self).__init__(cfg)
        self.reuse_generator = algorithms[cfg.reuse.algorithm](cfg, dataset)

    def explore(self): # TODO catch StopIteration
        m_goal = self.reuse_generator.next()
        return {'m_goal': m_goal, 'from': 'reuse'}
