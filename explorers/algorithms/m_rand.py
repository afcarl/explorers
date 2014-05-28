"""\
Pure random explorer.
Needs motor boundaries.
"""
from __future__ import absolute_import, division, print_function

from .. import explorer
from .. import tools

class RandomMotorExplorer(explorer.Explorer):
    """"""

    def explore(self):
        m_goal = tools.random_signal(self.m_channels)
        return {'m_goal': m_goal, 'from': 'motor.babbling'}
