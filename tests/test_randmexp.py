from __future__ import absolute_import, division, print_function, unicode_literals
import unittest
import random

import forest

import dotdot
from explorer import env
from explorer import explorers

class RandomEnv(env.Environment):

    def __init__(self, mbounds):
        self.m_channels = [env.Channel('order{}'.format(i), mb_i) for i, mb_i in enumerate(mbounds)]
        self.s_channels = [env.Channel('feedback0'),
                           env.Channel('feedback1'),
                           env.Channel('feedback3')]

    def execute(self, order):
        return [{c.name: random.random() for c in self.s_channels}]


class TestCoverage(unittest.TestCase):

    def test_coverage(self):

        mbounds = ((23, 34), (-3, -2))
        env = RandomEnv(mbounds)
        exp_cfg = forest.Tree()
        exp_cfg.m_channels = env.m_channels

        exp = explorers.RandomMotorExplorer(exp_cfg)

        for t in range(100):
            order    = exp.explore()
            self.assertTrue(all(mb_i_min <= o_i <= mb_i_max for (mb_i_min, mb_i_max), o_i in zip(mbounds, order.values())))
            feedback = env.execute(order)
            exp.receive(feedback)

if __name__ == '__main__':
    unittest.main()
