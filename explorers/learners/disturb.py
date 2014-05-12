from __future__ import absolute_import, division, print_function
import random
import numbers

import forest
from models import dataset

from . import learner


defcfg = learner.Learner.defcfg._copy(deep=True)
defcfg._describe('dist_width', instanceof=numbers.Real,
                 docstring='maximum distance of disturbance along each dimension')

class DisturbLearner(learner.Learner):
    """"""
    defcfg = defcfg

    def __init__(self, cfg):
        super(DisturbLearner, self).__init__(cfg)
        self.dataset = Dataset(len(self.m_channels), len(self.s_channels))

    def predict(self, data):
        """Predict the effect of an order"""
        return None

    def infer(self, data):
        """Infer the motor command to obtain an effect"""
        assert 'goal' in data
        goal = tools.to_tuple(data['goal'])
        dists, indexes = self.dataset.nn_y(goal, k = 1)
        nn_order = self.dataset.get_x(indexes[0])

        order = [v + random.uniform(-self.cfg.dist_with, self.cfg.dist_with) for v in nn_order]
        order = self._inflate_m_signal(tools.to_signal([min(max(v, 0.0), 1.0) for c in self.m_channels], self.m_channels))

        return order

    def update(self, observation):
        order = tools.to_tuple(self._deflate_m_signal((observations[0]['order'])))
        effect = tools.to_tuple(observations[1]['feedback'])
        dataset.add_xy(order, effect)
