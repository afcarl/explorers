# This is a minimal example for the explorers library.

from __future__ import absolute_import, division, print_function, unicode_literals
import random

import forest
import environments as envs

import dotdot
import explorers


class RandomEnv(envs.Environment):

    def __init__(self):
        self.m_channels = [envs.Channel('m_0', (  0.0, 1.0)),
                           envs.Channel('m_1', (-10.0, 0.0))]
        self.s_channels = [envs.Channel('feedback0'),
                           envs.Channel('feedback1'),
                           envs.Channel('feedback3')]

    def _execute(self, m_signal, meta=None):
        return {'s_signal': {c.name: random.random() for c in self.s_channels}}


env = RandomEnv()

exp_cfg = forest.Tree()
exp_cfg.m_channels = env.m_channels
exp = explorers.RandomMotorExplorer(exp_cfg)

for t in range(100):
    exploration = exp.explore()
    feedback    = env.execute(exploration)
    exp.receive(exploration, feedback)
