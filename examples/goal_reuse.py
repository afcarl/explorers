import random

import environments.envs
import learners

import dotdot
import explorers


random.seed(0)

ARM_DIM = 2
RES     = 20
N       = 2000


# Environment Config
env_cfg = environments.envs.KinematicArm2D.defcfg
env_cfg.dim = ARM_DIM
env_cfg.lengths = 1.0/env_cfg.dim


# Learner Config
learn_cfg = learners.DisturbLearner.defcfg._deepcopy()
learn_cfg.m_disturb = 0.05


# Source Explorer Config
ex_cfg              = explorers.MetaExplorer.defcfg._deepcopy()
ex_cfg.eras         = (10, None)
ex_cfg.weights      = ((1.0, 0.0), (0.0, 1.0))
ex_cfg.fallback     = 0
ex_cfg.ex_0         = explorers.RandomMotorExplorer.defcfg._deepcopy()
ex_cfg.ex_1         = explorers.RandomGoalExplorer.defcfg._deepcopy()
ex_cfg.ex_1.learner = learn_cfg


# Instanciating the Environment and the Explorer
env = environments.Environment.create(env_cfg)
# for c in env.m_channels:
#     c.bounds = (-15, 15)
# env.m_channels[0].bounds = (-150, 150)

ex_cfg.m_channels = env.m_channels
ex_cfg.s_channels = env.s_channels
ex = explorers.Explorer.create(ex_cfg)


# Running the Exploration
explorations = []
for i in range(N):
    exploration = ex.explore()
    feedback = env.execute(exploration['m_signal'])
    ex.receive(exploration, feedback)
    explorations.append((exploration, feedback))

dataset  = {'m_channels'  : ex.m_channels,
            's_channels'  : ex.s_channels,
            'explorations': explorations}


# Target Explorer Config
tgt_ex_cfg                = explorers.MetaExplorer.defcfg._deepcopy()
tgt_ex_cfg.eras           = (100, None)
tgt_ex_cfg.weights        = ((1.0, 0.0, 1.0, 1.0), (0.0, 1.0, 0.5, 0.5))
tgt_ex_cfg.fallback       = 0

tgt_ex_cfg.ex_0           = explorers.RandomMotorExplorer.defcfg._deepcopy()

tgt_ex_cfg.ex_1           = explorers.RandomGoalExplorer.defcfg._deepcopy()
tgt_ex_cfg.ex_1.learner   = learn_cfg

tgt_ex_cfg.ex_2           = explorers.ReuseExplorer.defcfg._deepcopy()
tgt_ex_cfg.ex_2.reuse.res = RES
tgt_ex_cfg.ex_2.learner   = learn_cfg

tgt_ex_cfg.ex_3           = explorers.GoalReuseExplorer.defcfg._deepcopy()
tgt_ex_cfg.ex_3.reuse.res = RES
tgt_ex_cfg.ex_3.learner   = learn_cfg


# Instanciating the Environment and the Explorer
env = environments.Environment.create(env_cfg)

tgt_ex_cfg.m_channels = env.m_channels
tgt_ex_cfg.s_channels = env.s_channels
tgt_ex = explorers.Explorer.create(tgt_ex_cfg, datasets=[dataset])


# Running the Target Exploration
tgt_explorations = []
for i in range(N):
    exploration = ex.explore()
    feedback = env.execute(exploration['m_signal'])
    tgt_ex.receive(exploration, feedback)
    tgt_explorations.append((exploration, feedback))

tgt_dataset  = {'m_channels'  : ex.m_channels,
                's_channels'  : ex.s_channels,
                'explorations': tgt_explorations}


# Graphs
try:
    from bokeh import plotting
    plotting.output_file('goal_reuse.html')


    xs = [explo[1]['s_signal']['x'] for explo in dataset['explorations']]
    ys = [explo[1]['s_signal']['y'] for explo in dataset['explorations']]
    plotting.scatter(xs, ys, x_range=[-1, 1], y_range=[-1, 1], title='explorers library: goal reuse algorithm example',
                     fill_alpha= 0.5, line_color=None, radius=2.0, radius_units='screen')
    plotting.show()

except ImportError:
    print('exploration went fine, but you need the bokeh library  (http://bokeh.pydata.org/) to display it')

