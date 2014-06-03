"""\
Pure random sensory explorer.
Needs motor and sensor boundaries.
"""
from __future__ import absolute_import, division, print_function
import random
import collections

import forest

from .. import conduits
from .. import explorer

defcfg = explorer.defcfg._copy(deep=True)
defcfg._describe('s_channels', instanceof=collections.Iterable,
                 docstring='Sensory channels to generate random goal from')

class MetaExplorer(explorer.Explorer):
    """\
    An explorer to orchestrate other explorers.
    """
    pass
