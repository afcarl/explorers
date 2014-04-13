from __future__ import division, print_function
import unittest
import random

import forest

import dotdot
import explorers
from explorers import envs

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

        reuse_cfg                 = explorers.ReuseExplorer.defcfg._copy(deep=True)
        reuse_cfg.m_channels      = env.m_channels
        reuse_cfg.s_channels      = [envs.Channel('feedback{}'.format(i), sb_i) for i, sb_i in enumerate(sbounds)]
        reuse_cfg.reuse.algorithm = 'sensor_uniform'
        reuse_cfg.reuse.ratio     = 1.0
        reuse_cfg.reuse.window    = (0, 500)
        reuse_cfg.reuse.res       = 10
        reuse_cfg._strict(True)

        reuse_explorer = explorers.ReuseExplorer(reuse_cfg, dataset)

        reuse_cfg._pop('s_channels')
        reuse_cfg.reuse.sbounds   = sbounds
        reuse_explorer = explorers.ReuseExplorer(reuse_cfg, dataset)

        for _ in range(500):
            order = reuse_explorer.explore()
            self.assertTrue(order['order'] in orders)

        for _ in range(500):
            order = reuse_explorer.explore()
            self.assertTrue(not order['order'] in orders)


if __name__ == '__main__':
    unittest.main()
