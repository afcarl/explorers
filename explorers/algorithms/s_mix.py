"""Explorer with a first phase of motor babbling and then a mixed phase
    of motor and goal babbling.
"""
from __future__ import absolute_import, division, print_function
import random
import collections

from .. import explorer
from . import s_rand


defcfg = s_rand.RandomGoalExplorer.defcfg._copy(deep=True)
defcfg._describe('s_explorers', isinstance=collections.Iterable,
                 docstring='list of sensory explorers configuration')
defcfg._describe('s_explorers_weights', isinstance=collections.Iterable,
                 docstring='list of weight for each explorers')

def roulette_wheel(proba):
    assert len(proba) >= 1
    """Given a vector p, return index i with probability p_i/sum(p).
    Elements of p are positive numbers.
    @param proba    list of positive numbers
    """
    sum_proba = sum(proba)
    if sum_proba == 0.0:
        return random.randint(0, len(proba)-1)

    dice = random.uniform(0., sum_proba)
    s, i = proba[0], 0
    while (i < len(proba)-1 and dice >= s):
        i += 1
        assert proba[i] >= 0, "all elements are not positive {}".format(proba)
        s += proba[i]
    return i


class MixedGoalExplorer(s_rand.RandomGoalExplorer):

    defcfg = defcfg

    def __init__(self, cfg, inv_learners=(), **kwargs):
        super(MixedGoalExplorer, self).__init__(cfg)
        assert len(self.cfg.explorers) == len(self.cfg.s_explorers_weights)

        self.s_explorers = []
        for s_explorer in self.cfg.s_explorers:
            class_ = explorer._load_class(s_explorer.classname)
            s_explorer._update(class_.defcfg, overwrite=False)
            s_explorer._update(self.cfg, described_only=True)
            self.s_explorers.append(class_(self.cfg.m_explorer))

    def explore(self):
        idx = roulette_wheel(self.cfg.s_explorers_weights)
        return self.s_explorers[i].explore()

    def receive(self, feedback):
        self.timecount += 1
        self.obs_conduit.receive(feedback)
        for s_explorer in self.s_explorers:
            s_explorer.receive(feedback)
