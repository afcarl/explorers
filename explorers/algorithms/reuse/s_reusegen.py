"""Reuse generators, that yield order to reuse"""

from __future__ import print_function, division, absolute_import
import random
import numbers
import collections

import scicfg

from ... import meshgrid
from ... import tools


DEBUG = False


rrcfg = scicfg.SciConfig(strict=True)
rrcfg._describe('reuse.s_channels', instanceof=collections.Iterable,
                docstring='bounds for the meshgrid')
rrcfg._describe('reuse.m_channels', instanceof=collections.Iterable,
                docstring='m_channels for the order metadata')
rrcfg._freeze(True)


class RandomReuse(object):
    """Random reuse"""

    defcfg = rrcfg

    def __init__(self, cfg, dataset, **kwargs):
        """"""
        self.cfg = cfg
        self.cfg.reuse.m_channels = dataset['m_channels']
        self.cfg.reuse.s_channels = dataset['s_channels']
        self._compute_ordering(dataset)

    @property
    def m_channels(self):
        return self.cfg.reuse.m_channels

    @property
    def s_channels(self):
        return self.cfg.reuse.s_channels

    def _compute_ordering(self, dataset):
        orders = [exploration['m_signal'] for exploration, feedback in dataset['explorations']]
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


eucfg = rrcfg._deepcopy()
eucfg._describe('reuse.res', instanceof=(numbers.Integral, collections.Iterable),
                docstring='resolution of the meshgrid')
eucfg._freeze(True)


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
        self.cfg.reuse.m_channels = dataset['m_channels']
        self.cfg.reuse.s_channels = dataset['s_channels']

        sbounds = [c.bounds for c in self.cfg.reuse.s_channels]

        self._meshgrid = meshgrid.MeshGrid(self.cfg.reuse, sbounds)
        self._compute_ordering(dataset)

    def _compute_ordering(self, dataset):
        for exploration, feedback in dataset['explorations']:
            s_vector = tools.to_vector(feedback['s_signal'], self.cfg.reuse.s_channels)
            self._meshgrid.add(s_vector, metadata=exploration['m_signal'])

        if DEBUG:
            for _, content in sorted(self._meshgrid._bins.items()):
                print('{}: {}'.format(content.bounds, len(content)))

        self.orders  = collections.deque()
        self.effects = collections.deque()
        for _ in range(len(dataset['explorations'])):
            effect, order = self._meshgrid.draw(replace=False, metadata=True)
            self.orders.append(order)
            self.effects.append(effect)


class PickOneReuse(SensorUniformReuse):

    def _compute_ordering(self, dataset):
        for exploration, feedback in dataset['explorations']:
            s_vector = tools.to_vector(feedback['s_signal'], self.cfg.reuse.s_channels)
            self._meshgrid.add(s_vector, metadata=exploration['m_signal'])

        self.orders  = collections.deque()
        for bin_ in self._meshgrid._nonempty_bins:
            _, _, m_signal = bin_.draw()
            self.orders.append(m_signal)
