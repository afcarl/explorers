"""Reuse generators, that yield order to reuse"""

from __future__ import print_function, division, absolute_import
import random
import numbers
import collections

import forest

from . import meshgrid


class RandomReuse(object):
    """Random reuse"""

    defcfg = forest.Tree()

    def __init__(self, cfg, dataset, **kwargs):
        """"""
        self.dataset   = dataset
        self._compute_ordering()

    def _compute_ordering(self):
        orders = [order for order, effect in self.dataset]
        self.orders = random.sample(orders, len(orders))

    def __iter__(self):
        return self

    def __len__(self):
        return len(self.orders)

    def __next__(self):
        try:
           return self.orders.pop()
        except IndexError:
            raise StopIteration

    def next(self):
        return self.__next__()


eucfg = forest.Tree(strict=True)
eucfg._describe('res', instanceof=(numbers.Integral, collections.Iterable),
                docstring='resolution of the meshgrid')
eucfg._describe('sbounds', instanceof=collections.Iterable,
                docstring='bounds for the meshgrid')


class SensorUniformReuse(RandomReuse):
    """\
    Effect uniform reuse.
    Uses a meshgrid to put motor commands into bin according to their effect
    distribution and draw order by selecting a non-empty bin at random.

    You can expect the begining of the distribution to be unifomrly distributed,
    but if you draw all elements, the tail will consist of only elements from the
    bins with the highest densities.
    """
    defcfg = eucfg

    def __init__(self, cfg, dataset):
        self.dataset = dataset
        self.cfg = cfg
        self._meshgrid = meshgrid.MeshGrid(cfg.sbounds, cfg.res)
        self._compute_ordering()

    def _compute_ordering(self):
        for order, effect in self.dataset:
            self._meshgrid.add(effect, metadata=order)

        self.orders  = []
        self.effects = []
        for _ in range(len(self.dataset)):
            effect, order = self._meshgrid.draw(replace=False, metadata=True)
            self.orders.append(order)
            self.effects.append(effect)
