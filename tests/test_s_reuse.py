from __future__ import division, print_function
import unittest
import random

import forest

import dotdot
import explorers
from explorers import envs
from explorers import learners

import testenvs


random.seed(0)


class TestReuse(unittest.TestCase):

    def test_reuseexp_random(self):
        mbounds = ((0, 1), (-1, 0))
        sbounds = ((4, 9),)

        env = testenvs.RandomEnv(mbounds)

        reuse_cfg                  = explorers.ReuseExplorer.defcfg._copy(deep=True)
        reuse_cfg.m_channels       = env.m_channels
        reuse_cfg.reuse.s_channels = [envs.Channel('feedback{}'.format(i), sb_i) for i, sb_i in enumerate(sbounds)]
        reuse_cfg.reuse.algorithm  = 'sensor_uniform'
        reuse_cfg.reuse.res        = 10
        reuse_cfg._strict(True)

        dataset = []
        orders  = []
        for _ in range(100):
            m = testenvs.random_signal(reuse_cfg.m_channels)
            s = testenvs.random_signal(reuse_cfg.reuse.s_channels)
            dataset.append((m, s))
            orders.append(m)

        reuse_explorer = explorers.ReuseExplorer(reuse_cfg, dataset)

        for _ in range(100):
            order = reuse_explorer.explore()
            self.assertTrue(order['order'] in orders)

        with self.assertRaises(StopIteration):
            reuse_explorer.explore()

    def test_reuseexp_random2(self):
        mbounds = ((0, 1), (-1, 0))
        sbounds = ((4, 9),)

        env = testenvs.RandomEnv(mbounds)

        reuse_cfg                  = explorers.ReuseExplorer.defcfg._copy(deep=True)
        reuse_cfg.m_channels       = env.m_channels
        reuse_cfg.reuse.s_channels = [envs.Channel('feedback{}'.format(i), sb_i) for i, sb_i in enumerate(sbounds)]
        reuse_cfg.reuse.algorithm  = 'sensor_uniform'
        reuse_cfg.reuse.res        = 10
        reuse_cfg._strict(True)

        dataset = []
        orders  = []
        for _ in range(1000):
            m = testenvs.random_signal(reuse_cfg.m_channels)
            s = testenvs.random_signal(reuse_cfg.reuse.s_channels)
            dataset.append((m, s))
            orders.append(m)


        reuse_explorer = explorers.ReuseExplorer(reuse_cfg, dataset)

        for _ in range(100):
            order = reuse_explorer.explore()
            self.assertTrue(order['order'] in orders)


    def test_mg_reuseexp(self):
        mbounds = ((0, 1), (-1, 0))
        sbounds = ((4, 9),)

        env = testenvs.RandomEnv(mbounds)

        reuse_cfg                  = explorers.ReuseExplorer.defcfg._copy(deep=True)
        reuse_cfg.m_channels       = env.m_channels
        reuse_cfg.reuse.s_channels = [envs.Channel('feedback{}'.format(i), sb_i) for i, sb_i in enumerate(sbounds)]
        reuse_cfg.reuse.algorithm  = 'sensor_uniform'
        reuse_cfg.reuse.res        = 10
        reuse_cfg._strict(True)

        dataset = []
        orders  = []
        for _ in range(1000):
            m = testenvs.random_signal(reuse_cfg.m_channels)
            s = testenvs.random_signal(reuse_cfg.reuse.s_channels)
            dataset.append((m, s))
            orders.append(m)

        reuse_explorer = explorers.ReuseExplorer(reuse_cfg, dataset)

        learner_cfg = learners.ModelLearner.defcfg._copy(deep=True)
        learner_cfg.m_channels = env.m_channels
        learner_cfg.s_channels = env.s_channels
        learner_cfg.models.fwd = 'LWLR'
        learner_cfg.models.inv = 'L-BFGS-B'

        learner = learners.ModelLearner(learner_cfg)

        explorr_cfg = explorers.MotorGoalExplorer.defcfg._copy(deep=True)
        explorr_cfg.m_channels = env.m_channels
        explorr_cfg.s_channels = env.s_channels
        explorr_cfg.mb_bootstrap = 120
        explorr_cfg.mb_ratio     = 0.3

        mg_explorer = explorers.MotorGoalExplorer(explorr_cfg, inv_learners=[learner], m_explorer=reuse_explorer)

        for _ in range(100):
            order = mg_explorer.explore()
            self.assertTrue(order['order'] in orders)

if __name__ == '__main__':
    unittest.main()
