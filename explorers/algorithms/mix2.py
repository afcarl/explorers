"""Explorer with a first phase of motor babbling and then a mixed phase
    of motor and goal babbling.
"""
from __future__ import absolute_import, division, print_function
import random
import numbers
import collections

from .. import conduits
from .. import tools
from .. import explorer


defcfg = explorer.Explorer.defcfg._copy(deep=True)
defcfg._describe('s_channels', instanceof=collections.Iterable,
                 docstring='Sensory channels of the explorer')
defcfg._branch('explorer_a')
defcfg._branch('explorer_b')
defcfg._describe('ratio_a', instanceof=numbers.Real,
                 docstring='the percentage with which explorer1 is used')
defcfg._describe('bootstrap_a', instanceof=numbers.Real, default=0,
                 docstring='how many initial exploration to do with only explorer_a')
defcfg._describe('permitted_a', instanceof=numbers.Real, default=1e308, # HACK
                 docstring='the last step where explorer_a can be used')
defcfg.classname = 'explorers.Mix2Explorer'


class Mix2Explorer(explorer.Explorer):

    defcfg = defcfg

    def __init__(self, cfg, **kwargs):
        super(Mix2Explorer, self).__init__(cfg, **kwargs)
        self.timecount = 0

        class_ = tools._load_class(self.cfg.explorer_a.classname)
        self.cfg.explorer_a._update(class_.defcfg, overwrite=False)
        exp_cfg = self.cfg.explorer_a._copy(deep=True)
        exp_cfg._update(self.cfg, overwrite=False, described_only=True)
        self.cfg.explorer_a = exp_cfg
        self.explorer_a = class_(self.cfg.explorer_a, **kwargs)
        self.exp_conduit.register(self.explorer_a)

        class_ = tools._load_class(self.cfg.explorer_b.classname)
        self.cfg.explorer_b._update(class_.defcfg, overwrite=False)
        exp_cfg = self.cfg.explorer_b._copy(deep=True)
        exp_cfg._update(self.cfg, overwrite=False, described_only=True)
        self.cfg.explorer_b = exp_cfg
        self.explorer_b = class_(self.cfg.explorer_b, **kwargs)
        self.exp_conduit.register(self.explorer_b)

    def _explore(self):
        if (self.timecount < self.cfg.permitted_a and
            (self.timecount < self.cfg.bootstrap_a or random.random() < self.cfg.ratio_a)):
            order = self.explorer_a.explore()
        else:
            order = self.explorer_b.explore()

        return order

    def receive(self, exploration, feedback):
        self.timecount += 1
        super(Mix2Explorer, self).receive(exploration, feedback)
