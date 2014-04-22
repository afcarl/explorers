"""Explorer with a first phase of motor babbling and then a mixed phase
    of motor and goal babbling.
"""
from __future__ import absolute_import, division, print_function
import random
import numbers
import collections

from .. import conduits
from . import explorer
from . import randgexp


defcfg = randgexp.RandomGoalExplorer.defcfg._copy(deep=True)
defcfg._branch('explorer_a')
defcfg._branch('explorer_b')
defcfg._describe('ratio_a', instanceof=numbers.Real,
                 docstring='the percentage with which explorer1 is used')
defcfg._describe('bootstrap_a', instanceof=numbers.Real,
                 docstring='how many initial exploration to do with only explorer_a')


class Mix2Explorer(randgexp.RandomGoalExplorer):

    defcfg = defcfg

    def __init__(self, cfg, inv_learners=()):
        super(MixedGoalExplorer, self).__init__(cfg)
        self.timecount = 0

        class_ = explorer._load_class(self.cfg.explorer_a.classname)
        self.cfg.explorer_a._update(class_.defcfg, overwrite=False)
        exp_cfg = self.cfg.explorer_a._copy(deep=True)
        exp_cfg._update(self.cfg, described_only=True)
        self.cfg.explorer_a = exp_cfg
        self.explorer_a = class_(self.cfg.explorer_a)

        class_ = explorer._load_class(self.cfg.explorer_b.classname)
        self.cfg.explorer_b._update(class_.defcfg, overwrite=False)
        exp_cfg = self.cfg.explorer_b._copy(deep=True)
        exp_cfg._update(self.cfg, described_only=True)
        self.cfg.explorer_b = exp_cfg
        self.explorer_b = class_(self.cfg.explorer_b)

    def explore(self):
        if self.timecount < self.a_bootstrap or random.random() < self.cfg.a_ratio:
            return self.explorer_a.explore()
        else:
            return self.explorer_b.explore()

    def receive(self, feedback):
        self.timecount += 1
        self.obs_conduit.receive(feedback)
        self.explorer_a.receive(feedback)
        self.explorer_b.receive(feedback)
