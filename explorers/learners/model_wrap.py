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
        self.cfg = cfg
        self.cfg._update(self.defcfg, overwrite=False)
        m_bounds = [(0.0, 1.0) if c.bounds[0] != c.bounds[1] else (0.0, 0.0) for c in self.m_channels]
        self.learner = models.learner.Learner(range(-len(self.m_channels), 0), range(len(self.s_channels)),
                                              m_bounds, fwd=self.cfg.models.fwd, inv=self.cfg.models.inv,
                                              **self.cfg.models.kwargs)

    def _inflate_m_signal(self, order):
        assert len(order) == len(self.m_channels)
        infl_order = collections.OrderedDict()
        for o_i, c_i in zip(order, self.m_channels):
            factor = 1.0
            if c_i.bounds[0] != c_i.bounds[1]:
                assert c_i.bounds[0] < c_i.bounds[1]
                factor = c_i.bounds[1] - c_i.bounds[0]
            infl_order[c_i.name] = o_i*factor + c_i.bounds[0]
        return infl_order

    def _deflate_m_signal(self, order):
        assert len(order) == len(self.m_channels)
        defl_order = []
        for c in self.m_channels:
            factor = 1.0
            if c.bounds[0] != c.bounds[1]:
                assert c.bounds[0] < c.bounds[1]
                factor = c.bounds[1] - c.bounds[0]
            defl_order.append((order[c.name]-c.bounds[0])/factor)
        return defl_order

    def predict(self, data):
        """Predict the effect of an order"""
        assert 'order' in data
        if self.m_names == set(data['order'].keys()):
            order = self._deflate_m_signal(data['order'])
            effect = self.learner.predict_effect(order)
            return collections.OrderedDict((c.name, e_i) for c, e_i in zip(self.s_channels, effect))

    def infer(self, data):
        """Infer the motor command to obtain an effect"""
        assert 'goal' in data
        if self.s_names >= set(data['goal'].keys()):
            order = self.learner.infer_order([data['goal'][c.name] for c in self.s_channels])
            return self._inflate_m_signal(order)

    def update(self, data):
        if data['uuid'] not in self.uuids:
            if (self.s_names <= set(data['feedback'].keys()) and
                self.m_names <= set(data['order'].keys())):
                self.uuids.add(data['uuid'])
                order  = tuple(self._deflate_m_signal(data['order']))
                effect = tuple(data['feedback'][c.name] for c in self.cfg.s_channels)
                self.learner.add_xy(order, effect)
