from __future__ import absolute_import, division, print_function
import random

import dotdot
from explorer import env

class RandomEnv(env.Environment):

    def __init__(self, mbounds):
        self.m_channels = [env.Channel('order{}'.format(i), mb_i) for i, mb_i in enumerate(mbounds)]
        self.s_channels = [env.Channel('feedback0'),
                           env.Channel('feedback1'),
                           env.Channel('feedback3')]

    def execute(self, order):
        return {'order':order,
                'feedback':{c.name: random.random() for c in self.s_channels}}

class BoundedRandomEnv(RandomEnv):

    def __init__(self, mbounds, sbounds):
        self.m_channels = [env.Channel('order{}'.format(i), mb_i) for i, mb_i in enumerate(mbounds)]
        self.s_channels = [env.Channel('feedback{}'.format(i), sb_i) for i, sb_i in enumerate(sbounds)]
