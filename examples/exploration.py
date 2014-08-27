import random

import environments.envs
import learners

import dotdot
import explorers


random.seed(0)


ARM_DIM = 20
RES = 25
N = 3000


# Environment Config

env_cfg = environments.envs.KinematicArm2D.defcfg
env_cfg.dim = ARM_DIM
env_cfg.lengths = 1.0/env_cfg.dim


# Learner Config

learn_cfg = learners.DisturbLearner.defcfg._deepcopy()
learn_cfg.m_disturb = 0.07


# Explorer Config

ex_cfg              = explorers.MetaExplorer.defcfg._deepcopy()
ex_cfg.eras         = (100, None)
ex_cfg.weights      = ((1.0, 0.0, 0.0), (0.0, 0.5, 0.5))
ex_cfg.fallback     = 2

ex_cfg.ex_0         = explorers.RandomMotorExplorer.defcfg._deepcopy()

ex_cfg.ex_1         = explorers.MeshgridGoalExplorer.defcfg._deepcopy()
ex_cfg.ex_1.learner = learn_cfg
ex_cfg.ex_1.res     = RES
ex_cfg.ex_1.cutoff  = 2

ex_cfg.ex_2         = explorers.UnreachGoalExplorer.defcfg._deepcopy()
ex_cfg.ex_2.learner = learn_cfg
ex_cfg.ex_2.res     = RES


# Instanciating the Environment and the Explorer

env = environments.Environment.create(env_cfg)

ex_cfg.m_channels = env.m_channels
ex_cfg.s_channels = env.s_channels
ex = explorers.Explorer.create(ex_cfg)


# Running the Exploration

exorations = []
for i in range(N):
    exploration = ex.explore()
    feedback = env.execute(exploration['m_signal'])
    ex.receive(exploration, feedback)
    exorations.append((exploration, feedback))

dataset  = {'m_channels'  : ex.m_channels,
            's_channels'  : ex.s_channels,
            'explorations': exorations}


# Graph

try:
    from bokeh import plotting
    plotting.output_file('reuse.html')


    xs = [explo[1]['s_signal']['x'] for explo in dataset['explorations']]
    ys = [explo[1]['s_signal']['y'] for explo in dataset['explorations']]
    plotting.scatter(xs, ys, x_range=[-1, 1], y_range=[-1, 1], title='explorers library: exploration example',
                     fill_alpha= 0.5, line_color=None, radius=2.0, radius_units='screen')
    #plotting.show()

except ImportError:
    print('exploration went fine, but you need the bokeh library to display the it')

