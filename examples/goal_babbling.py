import random

import environments.envs
import learners

import dotdot
import explorers


random.seed(0)


N = 2000 # how many timesteps


# Environment Config

env_cfg = environments.envs.KinematicArm2D.defcfg
env_cfg.dim = 20 # how many joints
env_cfg.lengths = 1.0/env_cfg.dim # lenghts of the segments between the joints
env_cfg.limits  = (-150, 150) # range of the joints in degrees


# Learner Config

learn_cfg = learners.DisturbLearner.defcfg._deepcopy()
learn_cfg.m_disturb = 0.05 # how much to perturbate the motor signals. Here, 5% of possible range (cf. env_cfg.limits)


# Explorer Config

ex_cfg              = explorers.MetaExplorer.defcfg._deepcopy()
ex_cfg.eras         = (10, None) # the end date of each era. The first eras ends at the 10th timestep.
ex_cfg.weights      = ((1.0, 0.0), (0.0, 1.0)) #
ex_cfg.fallback     = 2

ex_cfg.ex_0         = explorers.RandomMotorExplorer.defcfg._deepcopy()

ex_cfg.ex_1         = explorers.RandomGoalExplorer.defcfg._deepcopy()
ex_cfg.ex_1.learner = learn_cfg


# Instanciating the Environment and the Explorer

env = environments.Environment.create(env_cfg)

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


# Graph

# the red dots are from motor babbling
# the blue dots from goal babbling
try:
    from bokeh import plotting
    plotting.output_file('html/exploration.html')


    xs = [explo[1]['s_signal']['x'] for explo in dataset['explorations']]
    ys = [explo[1]['s_signal']['y'] for explo in dataset['explorations']]
    plotting.scatter(xs, ys, x_range=[-1, 1], y_range=[-1, 1], title='explorers library: exploration example',
                     fill_alpha= 0.5, line_color=None, radius=2.0, radius_units='screen')
    plotting.hold(True)
    plotting.scatter(xs[:ex_cfg.eras[0]], ys[:ex_cfg.eras[0]], x_range=[-1, 1], y_range=[-1, 1], title='explorers library: exploration example',
                     fill_alpha= 0.5, color='red', line_color=None, radius=2.0, radius_units='screen')
    plotting.show()

except ImportError:
    print('exploration went fine, but you need the bokeh library to display the it')

