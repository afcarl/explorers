"""Explorer with a first phase of motor babbling and then a mixed phase
    of motor and goal babbling.
"""
from __future__ import absolute_import, division, print_function
import random
import numbers
import collections

from .. import conduits
from . import explorer
from . import s_rand


defcfg = s_rand.RandomGoalExplorer.defcfg._copy(deep=True)
defcfg._branch('explorer_a')
defcfg._branch('explorer_b')
defcfg._describe('ratio_a', instanceof=numbers.Real,
                 docstring='the percentage with which explorer1 is used')
defcfg._describe('bootstrap_a', instanceof=numbers.Real,
                 docstring='how many initial exploration to do with only explorer_a')
defcfg._describe('permitted_a', instanceof=numbers.Real,
                 docstring='the last step where explorer_a can be used')
defcfg.bootstrap_a = 0
defcfg.permitted_a = 1e308 # HACK


class Mix2Explorer(s_rand.RandomGoalExplorer):

    defcfg = defcfg

    def __init__(self, cfg, inv_learners=(), **kwargs):
        super(Mix2Explorer, self).__init__(cfg, inv_learners=inv_learners)
        self.timecount = 0

        class_ = explorer._load_class(self.cfg.explorer_a.classname)
        self.cfg.explorer_a._update(class_.defcfg, overwrite=False)
        exp_cfg = self.cfg.explorer_a._copy(deep=True)
        exp_cfg._update(self.cfg, overwrite=False, described_only=True)
        self.cfg.explorer_a = exp_cfg
        self.explorer_a = class_(self.cfg.explorer_a, **kwargs)

        class_ = explorer._load_class(self.cfg.explorer_b.classname)
        self.cfg.explorer_b._update(class_.defcfg, overwrite=False)
        exp_cfg = self.cfg.explorer_b._copy(deep=True)
        exp_cfg._update(self.cfg, overwrite=False, described_only=True)
        self.cfg.explorer_b = exp_cfg
        self.explorer_b = class_(self.cfg.explorer_b, **kwargs)

    def explore(self):
        import explorers
        if isinstance(self.explorer_a, explorers.ReuseExplorer):
            print('reuse ?')
            print (self.timecount < self.cfg.permitted_a)
            print (self.timecount < self.cfg.bootstrap_a or random.random() < self.cfg.ratio_a)

        if (self.timecount < self.cfg.permitted_a and
            (self.timecount < self.cfg.bootstrap_a or random.random() < self.cfg.ratio_a)):
            order = self.explorer_a.explore()
        else:
            order = self.explorer_b.explore()

        if order['order'] is None:
            order['order'] = self._inv_request(order['goal'])
        return order

    def receive(self, feedback):
        self.timecount += 1
        self.obs_conduit.receive(feedback)
        self.explorer_a.receive(feedback)
        self.explorer_b.receive(feedback)
