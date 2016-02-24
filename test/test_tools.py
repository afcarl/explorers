from __future__ import division, print_function
import unittest
import random

import dotdot
import explorers
import explorers.tools

random.seed(0)


class TestTools(unittest.TestCase):

    def test_reuseexp_random(self):
        ex_cfg = explorers.MetaExplorer.defcfg._deepcopy()
        ex_cfg.eras      = (10, None)
        ex_cfg.weights   = ((0.0, 1.0), (1.0, 0.0))

        ex_cfg.ex_0         = explorers.RandomMotorExplorer.defcfg._deepcopy()

        ex_cfg.ex_1         = explorers.MeshgridGoalExplorer.defcfg._deepcopy()
        ex_cfg.ex_1.res     = 10

        s = explorers.tools.explorer_ascii(ex_cfg)
        self.assertTrue(len(s.split('\n')) > 1)

if __name__ == '__main__':
    unittest.main()
