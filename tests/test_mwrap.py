from __future__ import absolute_import, division, print_function
import unittest
import random

import forest

import dotdot
from explorer import explorers
from explorer import learners

import testenvs

class TestRandomGoalExplorer(unittest.TestCase):

    def test_simple(self):

        mbounds = ((23, 34), (-3, -2))
        sbounds = ((0, 1), (-1, -0), (101, 1001))
        env = testenvs.BoundedRandomEnv(mbounds, sbounds)
        exp_cfg = learners.ModelLearner.defcfg._copy(deep=True)
        exp_cfg.m_channels = env.m_channels
        exp_cfg.s_channels = env.s_channels
        exp_cfg.models.fwd = 'LWLR'
        exp_cfg.models.inv = 'L-BFGS-B'

        rndlearner = learners.ModelLearner(exp_cfg)
        exp = explorers.RandomGoalExplorer(exp_cfg, inv_learners=[rndlearner.infer])

        for t in range(100):
            order = exp.explore()
            self.assertTrue(all(mb_i_min <= o_i <= mb_i_max for (mb_i_min, mb_i_max), o_i in zip(mbounds, order['order'].values())))
            feedback = env.execute(order)
            exp.receive(feedback)

if __name__ == '__main__':
    unittest.main()
