"""\
Explorer base class
"""
from __future__ import absolute_import, division, print_function
import collections

import forest

from .. import conduits


defcfg = forest.Tree()
defcfg._describe('m_channels', instanceof=collections.Iterable,
                 docstring='Motor channels to generate random order of')

def _load_class(classname):
    module_name, class_name = classname.rsplit('.', 1)
    module = importlib.import_module(module_name)
    return getattr(module, class_name)


class Explorer(object):
    """"""
    defcfg = defcfg

    def create_explorer(cls, cfg):
        class_ = _load_class(cfg.classname)
        return class_(cfg)

    def __init__(self, cfg):
        self.cfg = cfg
        self.cfg._update(defcfg, overwrite=False)
        self.m_channels = cfg.m_channels
        self.obs_conduit = conduits.UnidirectionalHub()

    def explore(self):
        raise NotImplementedError

    def receive(self, feedback):
        self.obs_conduit.receive(feedback)
