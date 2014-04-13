from __future__ import absolute_import, division, print_function
import random

import dotdot
from explorers import envs

class RandomEnv(envs.Environment):

    def __init__(self, mbounds):
        self.m_channels = [envs.Channel('order{}'.format(i), mb_i) for i, mb_i in enumerate(mbounds)]
        self.s_channels = [envs.Channel('feedback0'),
                           envs.Channel('feedback1'),
                           envs.Channel('feedback3')]

    def execute(self, order):
        return {'order':order,
                'feedback':{c.name: random.random() for c in self.s_channels}}

class BoundedRandomEnv(RandomEnv):

    def __init__(self, mbounds, sbounds):
        self.m_channels = [envs.Channel('order{}'.format(i), mb_i) for i, mb_i in enumerate(mbounds)]
        self.s_channels = [envs.Channel('feedback{}'.format(i), sb_i) for i, sb_i in enumerate(sbounds)]
