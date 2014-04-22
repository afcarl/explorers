"""Reuse generators, that yield order to reuse"""

from __future__ import print_function, division, absolute_import
import random
import numbers
import collections

import forest

from . import s_reusegen
from .. import RandomMotorExplorer


algorithms = {'random'        : s_reusegen.RandomReuse,
              'sensor_uniform': s_reusegen.SensorUniformReuse}

defcfg = forest.Tree(strict=True)
defcfg._update(RandomMotorExplorer.defcfg)
defcfg._describe('reuse.s_channels', instanceof=collections.Iterable,
                 docstring='Sensory channels of the reused dataset')
defcfg._describe('reuse.algorithm', instanceof=str,
                 docstring='name of the reuse algorithm to use')
defcfg._describe('reuse.discount', instanceof=numbers.Real,
                 docstring='how much the ratio decrease with each reuse')

for algorithm in algorithms.values():
    defcfg._update(algorithm.defcfg)


class ReuseExplorer(RandomMotorExplorer):
    """A reuse explorer"""

    defcfg = defcfg

    def __init__(self, cfg, dataset=None, **kwargs):
        super(ReuseExplorer, self).__init__(cfg)
        self.cfg = cfg
        self.cfg._update(self.defcfg, overwrite=False)
        self.cfg.reuse.s_channels = dataset[0]
        self.reuse_generator = algorithms[cfg.reuse.algorithm](cfg, dataset[1])

    def explore(self): # TODO catch StopIteration
        order = self.reuse_generator.next()
        return {'order': order, 'type': 'reuse'}
