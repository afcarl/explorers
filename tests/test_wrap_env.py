from __future__ import absolute_import, division, print_function
import unittest
import random

import forest

import dotdot
import explorers
from explorers import envs

import testenvs

class SimpleEnv(object):

    def __init__(self):
        self.m_feats = (0, 1)
        self.m_bounds = ((0.0, 1.0), (0.0, 1.0))
        self.s_feats = (2, 3)

    def execute_order(self, order, meta=None):
        return (order[0] + order[1], order[0]*order[1])

    def close(self):
        pass


class TestEnvWrap(unittest.TestCase):

    def test_simple(self):

        sm_env = SimpleEnv()
        env  = envs.WrapEnvironment(sm_env)
        env2 = testenvs.SimpleEnv()
        exp = explorers.RandomMotorExplorer(env.cfg)

        for t in range(100):
            order    = exp.explore()
            self.assertEqual(order['type'], 'motorbabbling')
            self.assertTrue(all(mb_i_min <= o_i <= mb_i_max for (mb_i_min, mb_i_max), o_i in zip(sm_env.m_bounds, order['order'].values())))
            feedback  = env.execute(order['order'])
            feedback2 = env.execute(order['order'])
            self.assertEqual(feedback, feedback2)
            self.assertTrue('order' in feedback)
            self.assertTrue('feedback' in feedback)
            exp.receive(feedback)


if __name__ == '__main__':
    unittest.main()
