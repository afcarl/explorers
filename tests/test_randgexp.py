from __future__ import absolute_import, division, print_function, unicode_literals
import unittest
import random

import forest

import dotdot
from explorer import env
from explorer import explorers
from explorer import learners

import testenvs

class TestRandomGoalExplorer(unittest.TestCase):

    def test_simple(self):

        mbounds = ((23, 34), (-3, -2))
        sbounds = ((0, 1), (-1, -0), (101, 1001))
        env = testenvs.BoundedRandomEnv(mbounds, sbounds)
        exp_cfg = forest.Tree()
        exp_cfg.m_channels = env.m_channels
        exp_cfg.s_channels = env.s_channels

        rndlearner = learners.RandomLearner(exp_cfg)
        exp = explorers.RandomGoalExplorer(exp_cfg, inv_learners=[rndlearner.infer])

        for t in range(100):
            order = exp.explore()
            for (mb_i_min, mb_i_max), o_i in zip(mbounds, order.values()):
                print((mb_i_min, mb_i_max), o_i)
            self.assertTrue(all(mb_i_min <= o_i <= mb_i_max for (mb_i_min, mb_i_max), o_i in zip(mbounds, order.values())))
            feedback = env.execute(order)
            exp.receive(feedback)

if __name__ == '__main__':
    unittest.main()
