from __future__ import absolute_import, division, print_function
import random
import collections

import numpy as np

import forest

import dotdot
from explorers import envs


def random_signal(channels):
    return collections.OrderedDict((c.name, random.uniform(*c.bounds)) for c in channels)


class RandomEnv(envs.Environment):

    def __init__(self, mbounds):
        self.m_channels = [envs.Channel('order{}'.format(i), mb_i) for i, mb_i in enumerate(mbounds)]
        self.s_channels = [envs.Channel('feedback0'),
                           envs.Channel('feedback1'),
                           envs.Channel('feedback3')]

        self._cfg = forest.Tree()
        self._cfg.m_channels = self.m_channels
        self._cfg.s_channels = self.s_channels
        self._cfg._freeze(True)

    @property
    def cfg(self):
        return self._cfg

    def execute(self, order, meta=None):
        return {'order'   : order,
                'feedback':{c.name: random.random() for c in self.s_channels}}

class RandomLinear(RandomEnv):

    def __init__(self, m_bounds, s_dim):
        self.m = np.random.random((len(m_bounds), s_dim))

        self.m_channels = [envs.Channel('order{}'.format(i), mb_i) for i, mb_i in enumerate(m_bounds)]
        self.s_channels = [envs.Channel('feedback{}'.format(i)) for _ in range(s_dim)]

        self._cfg = forest.Tree()
        self._cfg.m_channels = self.m_channels
        self._cfg.s_channels = self.s_channels
        self._cfg._freeze(True)

    def execute(self, order, meta=None):
        m_vector = np.array([[order[c.name] for c in self.m_channels]])
        s_vector = ((self.m*m_vector.T).T)[0]
        effect = collections.OrderedDict((c.name, s_i) for c, s_i in zip(self.s_channels, s_vector))

        return {'order'   : order,
                'feedback': effect}



class SimpleEnv(RandomEnv):

    def __init__(self):
        m_bounds = ((0.0, 1.0), (0.0, 1.0))
        self.m_channels = [envs.Channel(i, mb_i) for i, mb_i in enumerate(m_bounds)]
        self.s_channels = [envs.Channel(i) for i in enumerate((2, 3))]

        self._cfg = forest.Tree()
        self._cfg.m_channels = self.m_channels
        self._cfg.s_channels = self.s_channels
        self._cfg._freeze(True)

    def execute(self, order, meta=None):
        effect = (order[0] + order[1], order[0]*order[1])
        return {'order'   : order,
                'feedback': {c.name: o_i for c, o_i in zip(self.s_channels,
                                                           effect          )}}


class BoundedRandomEnv(RandomEnv):

    def __init__(self, mbounds, sbounds):
        self.m_channels = [envs.Channel('order{}'.format(i), mb_i) for i, mb_i in enumerate(mbounds)]
        self.s_channels = [envs.Channel('feedback{}'.format(i), sb_i) for i, sb_i in enumerate(sbounds)]


assert issubclass(RandomEnv, envs.Environment)
assert issubclass(BoundedRandomEnv, envs.Environment)
