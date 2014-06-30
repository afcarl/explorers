"""\
Pure random explorer.
Needs motor boundaries.
"""
from __future__ import absolute_import, division, print_function

from .. import explorer
from .. import tools


defcfg = explorer.Explorer.defcfg._deepcopy()
defcfg.classname = 'explorers.RandomMotorExplorer'

class RandomMotorExplorer(explorer.Explorer):
    """"""

    defcfg = defcfg

    def explore(self):
        m_goal = tools.random_signal(self.m_channels)
        return {'m_goal': m_goal, 'from': 'motor.babbling'}
