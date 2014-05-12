from __future__ import absolute_import, division, print_function
import random
import collections

import forest

from . import learner

class RandomLearner(learner.Learner):
    """"""

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
