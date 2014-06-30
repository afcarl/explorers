"""Reuse generators, that yield order to reuse"""

from __future__ import print_function, division, absolute_import
import random
import numbers
import collections

import forest

from . import meshgrid
from ... import tools


DEBUG = False

class RandomReuse(object):
    """Random reuse"""

    defcfg = forest.Tree()

    def __init__(self, cfg, dataset, **kwargs):
        """"""
        self.dataset   = dataset
        self._compute_ordering()

    def _compute_ordering(self):
        orders = [feedback['m_signal'] for  feedback in self.dataset[1]]
        self.orders = collections.deque(random.sample(orders, len(orders)))

    def __iter__(self):
        return self

    def __len__(self):
        return len(self.orders)

    def __next__(self):
        try:
           return self.orders.popleft()
        except IndexError:
            raise StopIteration

    def next(self):
        return self.__next__()


eucfg = forest.Tree(strict=True)
eucfg._describe('reuse.res', instanceof=(numbers.Integral, collections.Iterable),
                docstring='resolution of the meshgrid')
eucfg._describe('reuse.s_channels', instanceof=collections.Iterable,
                docstring='bounds for the meshgrid')
eucfg._describe('reuse.m_channels', instanceof=collections.Iterable,
                docstring='m_channels for the order metadata')


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
        self.cfg = cfg
        self.cfg._update(self.defcfg, overwrite=False)
        self.cfg.reuse.m_channels = dataset[0][0]
        self.cfg.reuse.s_channels = dataset[0][1]
        self.dataset = dataset[1]

        sbounds = [c.bounds for c in self.cfg.reuse.s_channels]

        self._meshgrid = meshgrid.MeshGrid(sbounds, cfg.reuse.res)
        self._compute_ordering()

    def _compute_ordering(self):
        for feedback in self.dataset:
            s_vector = tools.to_vector(feedback['s_signal'], self.cfg.reuse.s_channels)
            self._meshgrid.add(s_vector, metadata=feedback['m_signal'])

        if DEBUG:
            for bounds, content in sorted(self._meshgrid._bins.items()):
                print('{}: {}'.format(content.bounds, len(content)))

        self.orders  = collections.deque()
        self.effects = collections.deque()
        for _ in range(len(self.dataset)):
            effect, order = self._meshgrid.draw(replace=False, metadata=True)
            self.orders.append(order)
            self.effects.append(effect)

