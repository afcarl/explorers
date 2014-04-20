"""Explorer with a first phase of motor babbling and then a mixed phase
    of motor and goal babbling.
"""
from __future__ import absolute_import, division, print_function
import random
import numbers

from .. import conduits
from .randgexp import RandomGoalExplorer
from .randmexp import RandomMotorExplorer


defcfg = RandomGoalExplorer.defcfg._copy(deep=True)
defcfg._describe('mb_bootstrap', instanceof=numbers.Integral,
                 docstring='the number of episodes of pure motor babbling at the beginning.')
defcfg._describe('mb_ratio', instanceof=numbers.Real,
                 docstring='the percentage of motor babbling during mixed exploration')
defcfg._describe('m_explorer_class', instanceof=str,
                 docstring='motor explorer class')
defcfg._describe('s_explorer_class', instanceof=str,
                 docstring='sensory explorer class')


class MotorGoalExplorer(RandomGoalExplorer):

    defcfg = defcfg

    def __init__(self, cfg, inv_learners=(), motor_explorer=None, goal_explorer=None):
        super(MotorGoalExplorer, self)
        self.mb_bootstrap = cfg.mb_bootstrap
        self.mb_ratio     = cfg.mb_ratio
        self.timecount = 0
        self.obs_conduit = conduits.UnidirectionalHub()
        self.motor_explorer = motor_explorer
        if self.motor_explorer is None:
            self.motor_explorer = RandomMotorExplorer(cfg)
        self.goal_explorer = goal_explorer
        if self.goal_explorer is None:
            self.goal_explorer = RandomGoalExplorer(cfg, inv_learners=inv_learners)

    def explore(self):
        if self.timecount < self.mb_bootstrap or random.random() < self.mb_ratio:
            return self.motor_explorer.explore()
        else:
            return self.goal_explorer.explore()

    def receive(self, feedback):
        self.timecount += 1
        self.obs_conduit.receive(feedback)
        self.goal_explorer.receive(feedback)
        self.motor_explorer.receive(feedback)
