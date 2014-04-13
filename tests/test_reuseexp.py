from __future__ import division, print_function
import unittest
import random

import forest

import dotdot
from explorers import reuse

import testenvs

random.seed(0)


class TestReuse(unittest.TestCase):

    def test_reuseexp_random(self):
        mbounds = ((0, 1), (-1, 0))
        sbounds = ((4, 9),)
        dataset = []
        orders  = []
        for _ in range(1000):
            m = [random.uniform(*b_i) for b_i in mbounds]
            s = [random.uniform(*b_i) for b_i in sbounds]
            dataset.append((m, s))
            orders.append(m)

        env = testenvs.RandomEnv(mbounds)

        reuse_cfg             = reuse.ReuseExplorer.defcfg._copy(deep=True)
        reuse_cfg.m_channels  = env.m_channels
        reuse_cfg.sbounds     = sbounds
        reuse_cfg.algorithm   = 'sensor_uniform'
        reuse_cfg.reuse_ratio = 1.0
        reuse_cfg.res         = 10
        reuse_cfg.window      = (0, 500)

        reuse_explorer = reuse.ReuseExplorer(reuse_cfg, dataset)

        for _ in range(500):
            order = reuse_explorer.explore()
            self.assertTrue(order['order'] in orders)

        for _ in range(500):
            order = reuse_explorer.explore()
            self.assertTrue(not order['order'] in orders)


if __name__ == '__main__':
    unittest.main()
