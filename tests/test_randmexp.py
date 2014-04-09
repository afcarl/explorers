from __future__ import absolute_import, division, print_function, unicode_literals
import unittest
import random

import forest

import dotdot
from explorer import env
from explorer import explorers

import testenvs

class TestRandomMotorExplorer(unittest.TestCase):

    def test_simple(self):

        mbounds = ((23, 34), (-3, -2))
        env = testenvs.RandomEnv(mbounds)
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
