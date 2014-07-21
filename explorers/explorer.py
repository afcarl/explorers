"""\
Explorer base class
"""
from __future__ import absolute_import, division, print_function
import collections
import abc

import forest

from . import conduits
from . import tools

defcfg = forest.Tree()
defcfg._describe('m_channels', instanceof=collections.Iterable,
                 docstring='Motor channels to generate random order of')
defcfg._describe('classname', instanceof=collections.Iterable,
                 docstring='The name of the explorer class. Only used with the create() class method.')


class Explorer(object):
    """"""
    __metaclass__ = abc.ABCMeta

    defcfg = defcfg

    @classmethod
    def create(cls, cfg, **kwargs):
        class_ = tools._load_class(cfg.classname)
        return class_(cfg, **kwargs)

    def __init__(self, cfg, **kwargs):
        if isinstance(cfg, dict):
            cfg = forest.Tree(cfg)
        self.cfg = cfg
        self.cfg._update(self.defcfg, overwrite=False)

        self.m_channels = cfg.m_channels
        self.obs_conduit = conduits.UnidirectionalHub()
        self.fwd_conduit = conduits.BidirectionalHub()
        self.inv_conduit = conduits.BidirectionalHub()


    @abc.abstractmethod
    def explore(self):
        raise NotImplementedError
        return {'m_goal': m_signal, # the actual motor command to try to execute in the environment.
                's_goal': s_signal, # if the motor command was generated a sensory goal, include this.
                'from': 'exploration.strategy'}

    def receive(self, feedback):
        assert isinstance(feedback, dict) and 'uuid' in feedback
        self.obs_conduit.receive(feedback)
