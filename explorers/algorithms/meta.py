"""\
Pure random sensory explorer.
Needs motor and sensor boundaries.
"""
from __future__ import absolute_import, division, print_function
import random
import collections

import forest

from .. import conduits
from .. import explorer
from .. import tools


defcfg = explorer.defcfg._deepcopy()
defcfg.classname = 'explorers.MetaExplorer'
defcfg._describe('s_channels', instanceof=collections.Iterable,
                 docstring='Sensory channels to generate random goal from')
defcfg._describe('eras', instanceof=collections.Iterable,
                 docstring='The end date of each era of orchestration')
defcfg._describe('weights', instanceof=collections.Iterable,
                 docstring='Relative weights of each explorer during each era. A list of weights per era.')
defcfg._branch('ex_0') # first explorer
#defcfg._branch('ex_1') # second explorer




class MetaExplorer(explorer.Explorer):
    """\
    An explorer to orchestrate other explorers.
    """

    defcfg = defcfg

    def __init__(self, cfg, **kwargs):
        super(MetaExplorer, self).__init__(cfg, **kwargs)
        self.timecount = 0
        self.current_era = 0
        self.explorers = []

        assert all(len(self.cfg.weights[0]) == len(w_i) for w_i in self.cfg.weights)

        for i, _ in enumerate(self.cfg.weights[0]):
            ex_cfg = self.cfg['ex_{}'.format(i)]
            ex_cfg._update(self.cfg, overwrite=False, described_only=True)
            self.explorers.append(explorer.Explorer.create(ex_cfg, **kwargs))

    def explore(self):
        if (self.timecount >= self.cfg.eras[self.current_era]):
            self.current_era += 1

        idx = tools.roulette_wheel(self.cfg.weights[self.current_era])
        return self.explorers[idx].explore()

    def receive(self, feedback):
        self.timecount += 1
        self.obs_conduit.receive(feedback)
        for ex in self.explorers:
            ex.receive(feedback)
