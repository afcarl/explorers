from __future__ import division, print_function
import unittest
import random

import forest

import dotdot
import explorers
import explorers.tools

import testenvs


random.seed(0)


class TestTools(unittest.TestCase):

    def test_reuseexp_random(self):
        goal_explorer = forest.Tree()
        goal_explorer._update(explorers.Mix2Explorer.defcfg, overwrite=False)
        goal_explorer.classname   = 'explorers.Mix2Explorer'
        goal_explorer.ratio_a     = 1.0
        goal_explorer.bootstrap_a = 0
        goal_explorer.explorer_a._update(explorers.RandomGoalExplorer.defcfg, overwrite=True)
        goal_explorer.explorer_a.classname  = 'explorers.RandomGoalExplorer'
        goal_explorer.explorer_b._update(explorers.MeshgridGoalExplorer.defcfg, overwrite=True)
        goal_explorer.explorer_b.classname  = 'explorers.MeshgridGoalExplorer'
        goal_explorer.explorer_b.res = 100

        print(explorers.tools.explorer_ascii(goal_explorer))

if __name__ == '__main__':
    unittest.main()
