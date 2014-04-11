from __future__ import absolute_import, division, print_function
import unittest
import random

import forest

import dotdot
from explorer.explorers.reuse import reusegen


random.seed(0)


class TestReuse(unittest.TestCase):

    def test_reuse_simple(self):
        mbounds = ((0, 1), (-1, 0))
        sbounds = ((4, 9),)
        dataset = []
        orders  = []
        for _ in range(1000):
            m = [random.uniform(*b_i) for b_i in mbounds]
            s = [random.uniform(*b_i) for b_i in sbounds]
            dataset.append((m, s))
            orders.append(m)

        reuse_cfg = reusegen.RandomReuse.defcfg._copy(deep=True)
        rndreuse = reusegen.RandomReuse(reuse_cfg, dataset)

        self.assertEqual(len(rndreuse), 1000)

        c = 0
        for mc in rndreuse:
            c += 1
            self.assertTrue(mc in orders)

        self.assertEqual(c, 1000)
        self.assertEqual(len(rndreuse), 0)


if __name__ == '__main__':
    unittest.main()
