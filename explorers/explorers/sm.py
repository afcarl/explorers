"""Explorer with a first phase of motor babbling and then a mixed phase
    of motor and goal babbling.
"""
from __future__ import absolute_import, division, print_function
import random
import numbers

from .. import conduits
from . import explorer
from . import randgexp


defcfg = randgexp.RandomGoalExplorer.defcfg._copy(deep=True)
defcfg._describe('mb_bootstrap', instanceof=numbers.Integral,
                 docstring='the number of episodes of pure motor babbling at the beginning.')
defcfg._describe('mb_ratio', instanceof=numbers.Real,
                 docstring='the percentage of motor babbling during mixed exploration')
defcfg._branch('m_explorer')
defcfg._branch('s_explorer')
defcfg.m_explorer.classname = 'explorers.RandomMotorExplorer'
defcfg.s_explorer.classname = 'explorers.RandomGoalExplorer'


class MotorGoalExplorer(randgexp.RandomGoalExplorer):

    defcfg = defcfg

    def __init__(self, cfg, inv_learners=(), m_explorer=None, s_explorer=None):
        super(MotorGoalExplorer, self).__init__(cfg)
        self.mb_bootstrap = self.cfg.mb_bootstrap
        self.mb_ratio     = self.cfg.mb_ratio
        self.timecount = 0

        self.m_explorer = m_explorer
        if self.m_explorer is None:
            class_ = explorer._load_class(self.cfg.m_explorer.classname)
            self.cfg.m_explorer._update(class_.defcfg, overwrite=False)
            m_exp_cfg = self.cfg.m_explorer._copy(deep=True)
            m_exp_cfg._update(self.cfg, described_only=True)
            self.cfg.m_explorer = m_exp_cfg
            self.m_explorer = class_(self.cfg.m_explorer)

        self.s_explorer = s_explorer
        if self.s_explorer is None:
            class_ = explorer._load_class(self.cfg.s_explorer.classname)
            self.cfg.s_explorer._update(class_.defcfg, overwrite=False)
            s_exp_cfg = self.cfg.s_explorer._copy(deep=True)
            s_exp_cfg._update(self.cfg, described_only=True)
            self.cfg.s_explorer = s_exp_cfg
            self.s_explorer = class_(self.cfg.s_explorer, inv_learners=inv_learners)

    def explore(self):
        if self.timecount < self.mb_bootstrap or random.random() < self.mb_ratio:
            return self.m_explorer.explore()
        else:
            return self.s_explorer.explore()

    def receive(self, feedback):
        self.timecount += 1
        self.obs_conduit.receive(feedback)
        self.m_explorer.receive(feedback)
        self.s_explorer.receive(feedback)
