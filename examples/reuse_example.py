
# coding: utf-8

## The Effect of the Reuse Algorithm

# This is a example of the reuse algorithm with two-dimensional arms.

# In[15]:

# comment this for different results
import random
random.seed(0)


### Exploration of the First Arm

# We instanciate a first arm with 20 segments of the same lenghts, with a total length of one meter.

# In[16]:

import environments.envs

ARM_DIM = 20

arm1_cfg = environments.envs.KinematicArm2D.defcfg._deepcopy()
arm1_cfg.dim = ARM_DIM
arm1_cfg.lengths = 1.0/arm1_cfg.dim

arm1 = environments.Environment.create(arm1_cfg)


# We create a goal babbling explorer that starts doing 10 random motor babbling exploration, and then does the 1990 following one by goal babbling.

# In[17]:

import explorers

MB_ERA = 50

ex1_cfg         = explorers.MetaExplorer.defcfg._deepcopy()
ex1_cfg.m_channels = arm1.m_channels
ex1_cfg.s_channels = arm1.s_channels

# two sub-explorer, motor babbling and goal babbling.
ex1_cfg.ex_0    = explorers.RandomMotorExplorer.defcfg._deepcopy()
ex1_cfg.ex_1    = explorers.RandomGoalExplorer.defcfg._deepcopy()
# the motor babbling eras ends at 50, the goal babbling never stops
ex1_cfg.eras    = (MB_ERA, None)
# the first sub-explorer is always used in the first eras, never in the second.
ex1_cfg.weights = ((1.0, 0.0), (0.0, 1.0))


# The goal babbling explorer needs an inverse model. We use a very simple one. Given a goal (i.e. a sensory signal), we find the nearest sensory signal in recorded observations, and then add a small random perturbation to its corresponding motor command to create a new motor command that we return.
#
# Here the perturbation is drawn between 5% of the legal value range of the motor channels.

# In[18]:

import learners

learn_cfg = learners.DisturbLearner.defcfg._deepcopy()
learn_cfg.m_disturb = 0.05
ex1_cfg.ex_1.learner = learn_cfg

ex1 = explorers.Explorer.create(ex1_cfg)


# We run the exploration policy for 2000 steps

# In[19]:

N = 2000

arm1_expls = []
for i in range(N):
    exploration = ex1.explore()
    feedback    = arm1.execute(exploration['m_signal'])
    ex1.receive(exploration, feedback)
    arm1_expls.append((exploration, feedback))

arm1_dataset = {'m_channels'  : arm1.m_channels,
                's_channels'  : arm1.s_channels,
                'explorations': arm1_expls}


# We show the scatter plot of the effects at time 200, 400, and 2000.

# In[20]:

from bokeh import plotting

plotting.output_file('html/reuse.html')


# In[21]:

arm1_xs = [e[1]['s_signal']['x'] for e in arm1_dataset['explorations']]
arm1_ys = [e[1]['s_signal']['y'] for e in arm1_dataset['explorations']]

def plot1(n=200):
    plotting.figure(title='arm1, {} steps'.format(n))
    plotting.scatter(arm1_xs[:n], arm1_ys[:n],
                     x_range=[-1, 1], y_range=[-1, 1],
                     fill_alpha= 0.5, line_color=None, radius=2.0, radius_units='screen')
#    plotting.show()


# In[22]:

plot1(n=50)
plot1(n=200)
plot1(n=N)


### Exploration of the Second Arm

# We instanciate the second arm. Each segment is 0.9 shorter than the previous one, but the total length is still one meter.

# In[23]:

arm2_cfg = environments.envs.KinematicArm2D.defcfg._deepcopy()
arm2_cfg.dim = ARM_DIM
arm2_cfg.lengths = [0.9**i for i in range(arm2_cfg.dim)]
arm2_cfg.lengths = [s/sum(arm2_cfg.lengths) for s in arm2_cfg.lengths]

arm2 = environments.Environment.create(arm2_cfg)


# If executing the same motor commands, the two arms's end-effector position is most of the time different.

# In[24]:

plotting.figure(title='arm motor commands examples')

from arm_vizu import bokeh_kin

# some sample motor signals
m_signals = [
    {'j0': -31.23, 'j1': -44.21, 'j2': -20.18, 'j3': +31.55, 'j4': +35.66, 'j5':  +5.19, 'j6': +17.34, 'j7': +24.51, 'j8':  -2.69, 'j9': +26.52, 'j10': -34.87, 'j11': +10.72, 'j12': -19.38, 'j13': -33.49, 'j14': +13.78, 'j15': -22.43, 'j16': +33.61, 'j17': -28.95, 'j18': +34.31, 'j19':   45.75},
    {'j0': -53.66, 'j1': -56.20, 'j2': -56.67, 'j3': -34.83, 'j4': -20.29, 'j5':  +7.51, 'j6': +20.92, 'j7': +25.51, 'j8': -17.59, 'j9':  +6.51, 'j10':  -9.65, 'j11': +45.70, 'j12': +20.88, 'j13': +24.25, 'j14': +28.65, 'j15': -42.79, 'j16': +34.45, 'j17': -39.90, 'j18':  +2.74, 'j19':  -11.12},
    {'j0': +58.13, 'j1': +45.43, 'j2': -21.01, 'j3':  +2.35, 'j4': -38.90, 'j5': -39.23, 'j6': +45.14, 'j7': -57.58, 'j8': +39.49, 'j9': +29.01, 'j10':  -0.09, 'j11': -56.19, 'j12': +56.07, 'j13':  +5.91, 'j14': +36.61, 'j15': -52.65, 'j16': -58.60, 'j17': +32.45, 'j18': +43.69, 'j19': -120.77},
    {'j0': +53.09, 'j1': +55.83, 'j2': -51.08, 'j3': +41.44, 'j4': +44.43, 'j5':  +4.67, 'j6':  +2.15, 'j7': +37.23, 'j8':  -3.77, 'j9': -46.70, 'j10': +56.41, 'j11': -21.08, 'j12': +13.73, 'j13': +47.23, 'j14':  +7.94, 'j15': -27.26, 'j16': +56.54, 'j17':  -7.77, 'j18': -18.98, 'j19': +149.46}
]

for i, m_signal in enumerate(m_signals):
    bokeh_kin(arm1, m_signal, alpha=0.2 + i*0.15)
    plotting.hold(True)
    bokeh_kin(arm2, m_signal, color='#91C46C', alpha=0.2 + i*0.15)
    plotting.hold(True)


# We instanciate the *reuse* explorer.

# In[25]:

ex2_cfg                = explorers.MetaExplorer.defcfg._deepcopy()
ex2_cfg.m_channels     = arm2.m_channels
ex2_cfg.s_channels     = arm2.s_channels

ex2_cfg.eras           = (MB_ERA, None)
ex2_cfg.weights        = ((1.0, 0.0), (0.0, 1.0))

ex2_cfg.ex_0           = explorers.ReuseExplorer.defcfg._deepcopy()
ex2_cfg.ex_0.reuse.res = 20 # the resolution of the meshgrid for reuse
ex2_cfg.ex_0.learner   = learn_cfg

ex2_cfg.ex_1           = explorers.RandomGoalExplorer.defcfg._deepcopy()
ex2_cfg.ex_1.learner   = learn_cfg

ex2 = explorers.Explorer.create(ex2_cfg, datasets=[arm1_dataset])


# In[26]:

arm2_expls = []
for i in range(N):
    exploration = ex2.explore()
    feedback    = arm2.execute(exploration['m_signal'])
    ex2.receive(exploration, feedback)
    arm2_expls.append((exploration, feedback))

arm2_dataset = {'m_channels'  : arm2.m_channels,
                's_channels'  : arm2.s_channels,
                'explorations': arm2_expls}


# In[27]:

arm2_xs = [e[1]['s_signal']['x'] for e in arm2_dataset['explorations']]
arm2_ys = [e[1]['s_signal']['y'] for e in arm2_dataset['explorations']]


# In[28]:

def plot2(n=200):
    plotting.figure(title='arm2 with reuse, {} steps'.format(n))
    plotting.scatter(arm2_xs[:n], arm2_ys[:n],
                     x_range=[-1, 1], y_range=[-1, 1],
                     fill_alpha=0.5, line_color=None, radius=2.0, radius_units='screen')
    #plotting.show()

plot2(n=50)
plot2(n=200)
plot2(n=N)

plotting.show()
# The effects transferred between step 0 and 50 cover the reachable space much better than random goal babbling could.
