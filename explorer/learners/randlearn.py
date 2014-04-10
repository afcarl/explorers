from __future__ import absolute_import, division, print_function, unicode_literals
import random
import sys
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
        self.s_channels = {c.name:c for c in cfg.s_channels}
        self.m_channels = {c.name:c for c in cfg.m_channels}
        self.s_names    = sorted(self.s_channels.keys())
        self.m_names    = sorted(self.m_channels.keys())

    def predict(self, data):
        """Predict the effect of an order"""
        assert 'order' in data
        if set(self.m_names) == set(data['order'].keys()):

            return {cname: random.uniform(*c.bounds) for cname, c in self.s_channels.items()}

    def infer(self, data):
        """Infer the motor command to obtain an effect"""
        assert 'goal' in data
        if set(self.s_names) >= set(data['goal'].keys()):
            return {cname: random.uniform(*c.bounds) for cname, c in self.m_channels.items()}

