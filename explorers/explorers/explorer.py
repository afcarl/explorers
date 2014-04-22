"""\
Explorer base class
"""
from __future__ import absolute_import, division, print_function
import collections
import importlib

import forest

from .. import conduits


defcfg = forest.Tree()
defcfg._describe('m_channels', instanceof=collections.Iterable,
                 docstring='Motor channels to generate random order of')
defcfg._describe('classname', instanceof=collections.Iterable,
                 docstring='The name of the explorer class. Only used with the create() class method.')

def _load_class(classname):
    module_name, class_name = classname.rsplit('.', 1)
    module = importlib.import_module(module_name)
    return getattr(module, class_name)


class Explorer(object):
    """"""
    defcfg = defcfg

    @classmethod
    def create(cls, cfg, **kwargs):
        class_ = _load_class(cfg.classname)
        return class_(cfg, **kwargs)

    def __init__(self, cfg, **kwargs):
        self.cfg = cfg
        self.cfg._update(defcfg, overwrite=False)
        self.m_channels = cfg.m_channels
        self.obs_conduit = conduits.UnidirectionalHub()

    def explore(self):
        raise NotImplementedError

    def receive(self, feedback):
        assert isinstance(feedback, dict)
        self.obs_conduit.receive(feedback)

    @classmethod
    def _to_vector(cls, signal, channels):
        assert len(signal) == len(channels)
        return cls._to_subvector(signal, channels)

    @classmethod
    def _to_subvector(cls, signal, channels):
        return tuple(signal[c.name] for c in channels)
