from __future__ import absolute_import, division, print_function
import random
import collections

import forest


defcfg = forest.Tree()
defcfg._describe('m_channels', instanceof=collections.Iterable,
                 docstring='Motor channels to generate random order of')
defcfg._describe('s_channels', instanceof=collections.Iterable,
                 docstring='Sensory channels to generate random goal from')

class RandomLearner(object):
    """"""
    defcfg = defcfg

    def __init__(self, cfg):
        self.s_channels = cfg.s_channels
        self.m_channels = cfg.m_channels
        self.s_names    = set(c.name for c in self.s_channels)
        self.m_names    = set(c.name for c in self.m_channels)

    def predict(self, data):
        """Predict the effect of an order"""
        assert 'order' in data
        if self.m_names == set(data['order'].keys()):
            return collections.OrderedDict((c.name, random.uniform(*c.bounds)) for c in self.s_channels)

    def infer(self, data):
        """Infer the motor command to obtain an effect"""
        assert 'goal' in data
        if self.s_names >= set(data['goal'].keys()):
            return collections.OrderedDict((c.name, random.uniform(*c.bounds)) for c in self.m_channels)

    def update(self, observation):
        pass

