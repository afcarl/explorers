from __future__ import absolute_import, division, print_function
import random
import collections

import forest

from .. import tools


defcfg = forest.Tree()
defcfg._describe('m_channels', instanceof=collections.Iterable,
                 docstring='Motor channels to generate random order of')
defcfg._describe('s_channels', instanceof=collections.Iterable,
                 docstring='Sensory channels to generate random goal from')
defcfg._describe('classname', instanceof=collections.Iterable,
                 docstring='The name of the learner class. Only used with the create() class method.')


class Learner(object):
    """"""
    defcfg = defcfg

    @classmethod
    def create(cls, cfg, **kwargs):
        class_ = tools._load_class(cfg.classname)
        return class_(cfg, **kwargs)

    def __init__(self, cfg):
        self.cfg = cfg
        self.s_channels = cfg.s_channels
        self.m_channels = cfg.m_channels
        self.s_names    = set(c.name for c in self.s_channels)
        self.m_names    = set(c.name for c in self.m_channels)
        self.uuids = set()

    def _deflate_m_signal(self, order):
        """Uniformize a motor signal"""
        assert len(order) == len(self.m_channels)
        defl_order = []
        for c in self.m_channels:
            factor = 1.0
            if c.bounds[0] != c.bounds[1]:
                assert c.bounds[0] < c.bounds[1]
                factor = c.bounds[1] - c.bounds[0]
            defl_order.append((order[c.name]-c.bounds[0])/factor)
        return defl_order

    def _inflate_m_signal(self, order):
        """Restore an uniformized motor signal"""
        assert len(order) == len(self.m_channels)
        infl_order = collections.OrderedDict()
        for o_i, c_i in zip(order, self.m_channels):
            factor = 1.0
            if c_i.bounds[0] != c_i.bounds[1]:
                assert c_i.bounds[0] < c_i.bounds[1]
                factor = c_i.bounds[1] - c_i.bounds[0]
            infl_order[c_i.name] = o_i*factor + c_i.bounds[0]
        return infl_order


    def predict(self, data):
        """Predict the effect of an order"""
        raise NotImplementedError

    def infer(self, data):
        """Infer the motor command to obtain an effect"""
        raise NotImplementedError

    def update(self, observation):
        raise NotImplementedError

    def __len__(self):
        return len(self.uuids)
