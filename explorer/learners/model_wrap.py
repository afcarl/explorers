"""A Wrapper class for `models` learners."""
from __future__ import absolute_import, division, print_function
import collections

import forest
import models.learner

from .randlearn import RandomLearner


defcfg = forest.Tree(strict=True)
defcfg._describe('m_channels', instanceof=collections.Iterable,
                 docstring='Motor channels to generate random order of')
defcfg._describe('s_channels', instanceof=collections.Iterable,
                 docstring='Sensory channels to generate random goal from')
defcfg._describe('models.fwd', instanceof=str,
                 docstring='The name of the forward model to use')
defcfg._describe('models.inv', instanceof=str,
                 docstring='The name of the invserse model to use')
defcfg._describe('models.kwargs', instanceof=dict,
                 docstring='optional keyword arguments')
defcfg.models.kwargs = {}

class ModelLearner(RandomLearner):
    """\
    Interface to models for explorer communications

    Note that we use predict() and infer() method names instead of
    predict_effect() and infer_order() of models.
    """
    defcfg = defcfg

    def __init__(self, cfg):
        super(ModelLearner, self).__init__(cfg)
        self.learner = models.learner.Learner(range(-len(self.m_channels), 0), range(len(self.s_channels)),
                                              [c.bounds for c in self.m_channels],
                                              fwd=cfg.models.fwd, inv=cfg.models.inv, **cfg.models.kwargs)

    def predict(self, data):
        """Predict the effect of an order"""
        assert 'order' in data
        if self.m_names == set(data['order'].keys()):
            effect = self.learner.predict_effect([data['order'][name] for name in self.m_names])
            return collections.OrderedDict((c.name, e_i) for c, e_i in zip(self.s_channels, effect))

    def infer(self, data):
        """Infer the motor command to obtain an effect"""
        assert 'goal' in data
        if self.s_names >= set(data['goal'].keys()):
            order = self.learner.infer_order([data['goal'][name] for name in self.s_names])
            return collections.OrderedDict((c.name, o_i) for c, o_i in zip(self.m_channels, order))
