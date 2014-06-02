from __future__ import absolute_import, division, print_function
import unittest
import random

import forest

import dotdot
import explorers
import learners

import environments as envs
from explorers import tools

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
            m = tools.random_signal(reuse_cfg.m_channels)
            s = tools.random_signal(reuse_cfg.reuse.s_channels)
            dataset.append((m, s))
            orders.append(m)

        reuse_explorer = explorers.ReuseExplorer(reuse_cfg, (env.s_channels, dataset))

        for _ in range(100):
            order = reuse_explorer.explore()
            self.assertTrue(order['m_goal'] in orders)

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
            m = tools.random_signal(reuse_cfg.m_channels)
            s = tools.random_signal(reuse_cfg.reuse.s_channels)
            dataset.append((m, s))
            orders.append(m)


        reuse_explorer = explorers.ReuseExplorer(reuse_cfg, (env.s_channels, dataset))

        for _ in range(100):
            order = reuse_explorer.explore()
            self.assertTrue(order['m_goal'] in orders)


if __name__ == '__main__':
    unittest.main()
