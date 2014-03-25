from __future__ import absolute_import, division, print_function, unicode_literals
import random

import forest

import sample_env
from explorer import env
from explorer import explorers


class RandomEnv(env.Environment):

    def __init__(self):
        self.m_channels = [env.Channel('order0', (  0.0, 1.0)),
                           env.Channel('order1', (-10.0, 0.0))]
        self.s_channels = [env.Channel('feedback0'),
                           env.Channel('feedback1'),
                           env.Channel('feedback3')]

    def execute(self, order):
        return [{c.name: random.random() for c in self.s_channels}]


env = RandomEnv()

exp_cfg = forest.Tree()
exp_cfg.m_channels = env.m_channels
exp = explorers.RandomExplorer(exp_cfg)

for t in range(100):
    order    = exp.explore()
    feedback = env.execute(order)
    exp.receive(feedback)
