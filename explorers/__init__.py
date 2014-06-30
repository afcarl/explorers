from __future__ import absolute_import

from .channels import Channel
from .explorer import Explorer

from .algorithms.reuse import MeshGrid

from .algorithms.m_rand    import RandomMotorExplorer
from .algorithms.s_rand    import RandomGoalExplorer
from .algorithms.s_mesh    import MeshgridGoalExplorer
from .algorithms.s_unreach import UnreachGoalExplorer
from .algorithms.mix2      import Mix2Explorer
from .algorithms.reuse     import ReuseExplorer
from .algorithms.s_set     import GoalSetExplorer
