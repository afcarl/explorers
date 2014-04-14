from __future__ import absolute_import, division, print_function, unicode_literals
import collections

import forest

from . import channels
from . import env

class WrapEnvironment(env.Environment):
    """\
    Wrap an environment with s_feats, m_feats and m_bounds property.

    If s_bounds is present, it is taken into account too.
    """
    OrderNotExecutableError = env.Environment.OrderNotExecutableError

    def __init__(self, sm_env):
        self.sm_env = sm_env

        self.m_channels = tuple(channels.Channel(mf_i, mb_i)
                                for mf_i, mb_i in zip(self.sm_env.m_feats,
                                                      self.sm_env.m_bounds))

        try:
            s_bounds = self.sm_env.s_bounds
        except AttributeError:
            s_bounds = [None for _ in self.sm_env.s_feats]
        self.s_channels = tuple(channels.Channel(sf_i, sb_i)
                                for sf_i, sb_i in zip(self.sm_env.s_feats,
                                                      s_bounds))

        self._cfg = forest.Tree()
        self._cfg.m_channels = self.m_channels
        self._cfg.s_channels = self.s_channels
        self._cfg._freeze(True)

    @property
    def cfg(self):
        return self._cfg

    def execute(self, order):
        sm_order = tuple(order[c.name] for c in self.m_channels)
        sm_feedback = self.sm_env.execute_order(sm_order)
        return {'order': order,
                'feedback': collections.OrderedDict((c.name,f_i) for c, f_i in zip(self.s_channels, sm_feedback))}

    def close(self):
        self.sm_env.close()
