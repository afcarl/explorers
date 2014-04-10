"""Explorer with a first phase of motor babbling and then a mixed phase
    of motor and goal babbling.
"""
from __future__ import absolute_import, division, print_function
import random
import collections
import numbers

from .. import conduits
from .randgexp import RandomGoalExplorer
from .randmexp import RandomMotorExplorer


defcfg = RandomGoalExplorer.defcfg._copy(deep=True)
defcfg._describe('mb_bootstrap', instanceof=numbers.Integral,
                 docstring='the number of episodes of pure motor babbling at the beginning.')
defcfg._describe('mb_ratio', instanceof=numbers.Real,
                 docstring='the percentage of motor babbling during mixed exploration')


class MotorGoalExplorer(RandomGoalExplorer):

    def __init__(self, cfg, inv_learners = []):
        super(MotorGoalExplorer, self)
        self.mb_bootstrap = cfg.mb_bootstrap
        self.mb_ratio     = cfg.mb_ratio
        self.timecount = 0
        self.obs_conduit = conduits.UnidirectionalHub()
        self.goal_explorer = RandomGoalExplorer(cfg, inv_learners)
        self.motor_explorer = RandomMotorExplorer(cfg)

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
