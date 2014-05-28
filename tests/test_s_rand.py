from __future__ import absolute_import, division, print_function
import unittest
import random

import forest

import dotdot
import learners
import explorers

import testenvs

class TestRandomGoalExplorer(unittest.TestCase):

    def test_s_rand(self):

        mbounds = ((23, 34), (-3, -2))
        sbounds = ((0, 1), (-1, -0), (101, 1001))
        env = testenvs.BoundedRandomEnv(mbounds, sbounds)
        exp_cfg = learners.RandomLearner.defcfg._copy(deep=True)
        exp_cfg.m_channels = env.m_channels
        exp_cfg.s_channels = env.s_channels

        rndlearner = learners.RandomLearner(exp_cfg)
        exp = explorers.RandomGoalExplorer(exp_cfg, inv_learners=[rndlearner])

        for t in range(100):
            order = exp.explore()

            self.assertTrue(all(c.bounds[0] <= order['m_goal'][c.name] <= c.bounds[1] for c in env.m_channels))
            feedback = env.execute(order)
            exp.receive(feedback)

    def test_learner_cfg(self):

        mbounds = ((23, 34), (-3, -2))
        sbounds = ((0, 1), (-1, -0), (101, 1001))
        env = testenvs.BoundedRandomEnv(mbounds, sbounds)
        exp_cfg = forest.Tree()
        exp_cfg.m_channels = env.m_channels
        exp_cfg.s_channels = env.s_channels
        exp_cfg._branch('learner')
        exp_cfg.learner['m_channels'] = env.m_channels
        exp_cfg.learner['s_channels'] = env.s_channels
        exp_cfg.learner['models.fwd'] = 'LWLR'
        exp_cfg.learner['models.inv'] = 'L-BFGS-B'

        exp = explorers.RandomGoalExplorer(exp_cfg, inv_learners=())

        for t in range(100):
            order = exp.explore()
            print(order)
            self.assertTrue(all(c.bounds[0] <= order['m_goal'][c.name] <= c.bounds[1] for c in env.m_channels))
            feedback = env.execute(order)
            exp.receive(feedback)

if __name__ == '__main__':
    unittest.main()
