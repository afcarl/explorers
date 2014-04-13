"""Reuse generators, that yield order to reuse"""

from __future__ import print_function, division, absolute_import
import random
import numbers
import collections

import forest

from . import reusegen
from .. import RandomMotorExplorer


algorithms = {'random': reusegen.RandomReuse,
              'sensor_uniform': reusegen.SensorUniformReuse}

defcfg = forest.Tree(strict=True)
defcfg._update(RandomMotorExplorer.defcfg)
defcfg._describe('reuse.algorithm', instanceof=str,
                 docstring='name of the reuse algorithm to use')
defcfg._describe('reuse.ratio', instanceof=numbers.Real,
                 docstring='the percentage of motor reuse that should be used')
defcfg._describe('reuse.window', instanceof=collections.Iterable,
                 docstring='the period where the reuse should take place')
defcfg._describe('reuse.discount', instanceof=numbers.Real,
                 docstring='how much the ratio decrease with each reuse')

for algorithm in algorithms.values():
    defcfg._update(algorithm.defcfg)


class ReuseExplorer(RandomMotorExplorer):
    """A reuse explorer"""

    defcfg = defcfg

    def __init__(self, cfg, dataset=None):
        super(ReuseExplorer, self).__init__(cfg)
        self.cfg = cfg
        self.cfg._update(self.defcfg)
        self.reuse_generator = algorithms[cfg.reuse.algorithm](cfg, dataset)
        self.timecount = 0

    def explore(self):
        if self.cfg.reuse.window[0] <= self.timecount < self.cfg.reuse.window[1]:
            if random.random() < self.cfg.reuse.ratio:
                order = self.reuse_generator.next()
                exploration = {'order': order, 'type': 'reuse'}
        else:
            exploration = super(ReuseExplorer, self).explore()
        self.timecount += 1
        return exploration
