from __future__ import absolute_import, division, print_function
import unittest
import random

import forest

import dotdot
from explorer import env
from explorer import explorers
from explorer import learners

import testenvs

class TestRandomGoalExplorer(unittest.TestCase):

    def test_randgexp(self):

        mbounds = ((23, 34), (-3, -2))
        sbounds = ((0, 1), (-1, -0), (101, 1001))
        env = testenvs.BoundedRandomEnv(mbounds, sbounds)
        exp_cfg = learners.RandomLearner.defcfg._copy(deep=True)
        exp_cfg.m_channels = env.m_channels
        exp_cfg.s_channels = env.s_channels

        rndlearner = learners.RandomLearner(exp_cfg)
        exp = explorers.RandomGoalExplorer(exp_cfg, inv_learners=[rndlearner.infer])

        for t in range(100):
            order = exp.explore()
            self.assertTrue(all(mb_i_min <= o_i <= mb_i_max for (mb_i_min, mb_i_max), o_i in zip(mbounds, order['order'].values())))
            feedback = env.execute(order)
            exp.receive(feedback)

    def test_mgexp(self):

        mbounds = ((23, 34), (-3, -2), (-20, -19))
        sbounds = ((0, 1), (-1, -0), (101, 1001))
        env = testenvs.BoundedRandomEnv(mbounds, sbounds)

        learner_cfg = learners.ModelLearner.defcfg._copy(deep=True)
        learner_cfg.m_channels = env.m_channels
        learner_cfg.s_channels = env.s_channels
        learner_cfg.models.fwd = 'LWLR'
        learner_cfg.models.inv = 'L-BFGS-B'

        explorr_cfg = explorers.MotorGoalExplorer.defcfg._copy(deep=True)
        explorr_cfg.m_channels = env.m_channels
        explorr_cfg.s_channels = env.s_channels
        explorr_cfg.mb_bootstrap = 10
        explorr_cfg.mb_ratio     = 0.3

        learner = learners.ModelLearner(learner_cfg)
        exp = explorers.MotorGoalExplorer(explorr_cfg, inv_learners=[learner.infer])

        for t in range(100):
            order = exp.explore()
            if order['type'] == 'goalbabbling':
                self.assertTrue(all(sb_i_min <= o_i <= sb_i_max for (sb_i_min, sb_i_max), o_i in zip(sbounds, order['goal'].values())))
            self.assertTrue(all(mb_i_min <= o_i <= mb_i_max for (mb_i_min, mb_i_max), o_i in zip(mbounds, order['order'].values())))
            feedback = env.execute(order)
            exp.receive(feedback)


if __name__ == '__main__':
    unittest.main()
