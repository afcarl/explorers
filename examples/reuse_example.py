import random

from bokeh import plotting

import explorers
import environments

import dotdot
from expl import explorer_map
from envs import envs as env_map


random.seed(0)
plotting.output_file('reuse.html')
#plotting.output_server('Reuse: Basic Idea')

n_rm = 200
n    = 2000
stops = [200, 400, n]


# Source

src_kin = environments.Environment.create(env_map['kin20'])

src_cfg = explorer_map['disturb07']._deepcopy()
src_cfg.m_channels = src_kin.m_channels
src_cfg.s_channels = src_kin.s_channels
src_cfg.eras     = (n_rm, None)
src_cfg.weights = ((1.0, 0.0, 0.0), (0.1, 0.9, 0.0))
src_expl = explorers.Explorer.create(src_cfg)


src_explorations = []
for i in range(n):
    exploration = src_expl.explore()
    feedback = src_kin.execute(exploration['m_signal'])
    src_expl.receive(exploration, feedback)
    src_explorations.append((exploration, feedback))

src_dataset  = {'m_channels'  : src_kin.m_channels,
                's_channels'  : src_kin.s_channels,
                'explorations': src_explorations}


# Source graph
src_xs = [explo[1]['s_signal']['x'] for explo in src_dataset['explorations']]
src_ys = [explo[1]['s_signal']['y'] for explo in src_dataset['explorations']]
for stop in stops:
    name = 'source {}'.format(stop)
    plotting.scatter(src_xs[:stop], src_ys[:stop], x_range=[-1, 1], y_range=[-1, 1], title=name, filename=name, tools='',
                     fill_alpha= 0.5, line_color=None, radius=2.0, radius_units='screen')


# Reuse

reuse_cfg = explorers.ReuseExplorer.defcfg._deepcopy()
reuse_cfg.m_channels = src_kin.m_channels
reuse_cfg.s_channels = src_kin.s_channels
reuse_cfg.reuse.algorithm  = 'pickone'
reuse_cfg.reuse.res  = 8

reuse_expl = explorers.Explorer.create(reuse_cfg, datasets=[src_dataset])
reuse_explorations = []
for m_signal in reuse_expl.reuse_generator.orders:
    feedback = src_kin.execute(m_signal)
    reuse_explorations.append(({'m_signal': m_signal}, feedback))


reuse_dataset = {'m_channels'  : src_kin.m_channels,
                 's_channels'  : src_kin.s_channels,
                 'explorations': reuse_explorations}

# Reuse graph
#   # Grid
plotting.rect([0.0], [0.0], [2.0], [2.0], title='reuse',
              fill_color='#D8D8D8', line_color=None, x_range=[-1, 1], y_range=[-1, 1], tools='')
plotting.xgrid().grid_line_color = None
plotting.xaxis().major_tick_in   = 0
plotting.ygrid().grid_line_color = None
plotting.yaxis().major_tick_in   = 0
plotting.hold(True)

res = reuse_cfg.reuse.res
width = 2.0/res
x_rect, y_rect = [], []
for i in range(res):
    for j in range(res):
        x_rect.append(-1.0 + 0.5*width + width*i)
        y_rect.append(-1.0 + 0.5*width + width*j)

plotting.rect(x_rect, y_rect, [width-0.005]*res*res, [width-0.005]*res*res, x_range=[-1, 1], y_range=[-1, 1], fill_color='#FFFFFF', line_color=None)

#   #  Scatter
plotting.scatter(src_xs, src_ys, x_range=[-1, 1], y_range=[-1, 1],
                 fill_alpha= 0.5, line_color=None, radius=2.0, radius_units='screen')
reuse_xs = [explo[1]['s_signal']['x'] for explo in reuse_dataset['explorations']]
reuse_ys = [explo[1]['s_signal']['y'] for explo in reuse_dataset['explorations']]
plotting.scatter(reuse_xs, reuse_ys, x_range=[-1, 1], y_range=[-1, 1],
                 fill_alpha=0.0, line_color='red', radius=4.0, radius_units='screen', color=None)
plotting.hold(False)



# Target

tgt_kin = environments.Environment.create(env_map['kin20_09'])


tgt_reuse_explorations = []
for exploration, feedback in reuse_dataset['explorations']:
    m_signal = exploration['m_signal']
    feedback = tgt_kin.execute(m_signal)
    tgt_reuse_explorations.append(({'m_signal': m_signal}, feedback))

tgt_reuse_dataset = {'m_channels'  : src_kin.m_channels,
                     's_channels'  : src_kin.s_channels,
                     'explorations': tgt_reuse_explorations}


tgt_cfg = explorer_map['disturb2.07_reuse']._deepcopy()
tgt_cfg.m_channels = tgt_kin.m_channels
tgt_cfg.s_channels = tgt_kin.s_channels
tgt_cfg.ex_1.reuse.res = 8
tgt_cfg.eras = (n_rm, None)
tgt_cfg.weights      = ((0.5, 0.5, 0.0, 0.0), (0.05, 0.05, 0.9, 0.0))

tgt_expl = explorers.Explorer.create(tgt_cfg, datasets=[reuse_dataset])

tgt_explorations = []
for _ in range(n):
    exploration = tgt_expl.explore()
    feedback = tgt_kin.execute(exploration['m_signal'])
    tgt_expl.receive(exploration, feedback)
    tgt_explorations.append((exploration, feedback))


tgt_dataset = {'m_channels'  : src_kin.m_channels,
               's_channels'  : src_kin.s_channels,
               'explorations': tgt_explorations}
tgt_reuse_xs = [explo[1]['s_signal']['x'] for explo in tgt_reuse_dataset['explorations']]
tgt_reuse_ys = [explo[1]['s_signal']['y'] for explo in tgt_reuse_dataset['explorations']]


# Target graph
tgt_xs = [explo[1]['s_signal']['x'] for explo in tgt_dataset['explorations']]
tgt_ys = [explo[1]['s_signal']['y'] for explo in tgt_dataset['explorations']]
for i, stop in enumerate(stops):

    plotting.scatter(tgt_xs[:stop], tgt_ys[:stop], x_range=[-1, 1], y_range=[-1, 1], title='target {}'.format(stop),
                     fill_alpha= 0.5, line_color=None, radius=2.0, radius_units='screen', tools='')
    plotting.hold(True)
    if i == 0:
        plotting.scatter(tgt_reuse_xs, tgt_reuse_ys, x_range=[-1, 1], y_range=[-1, 1],
                     fill_alpha=0.0, line_color='red', radius=4.0, radius_units='screen', color=None)
    plotting.hold(False)

plotting.show()



# Target with no reuse graph

tgt_noreuse_kin = environments.Environment.create(env_map['kin20_09'])

tgt_noreuse_cfg = explorer_map['disturb07']._deepcopy()
tgt_noreuse_cfg.m_channels = tgt_noreuse_kin.m_channels
tgt_noreuse_cfg.s_channels = tgt_noreuse_kin.s_channels
tgt_noreuse_cfg.eras     = (n_rm, None)
tgt_noreuse_cfg.weights = ((1.0, 0.0, 0.0), (0.1, 0.9, 0.0))
tgt_noreuse_expl = explorers.Explorer.create(tgt_noreuse_cfg)


tgt_noreuse_explorations = []
for i in range(n):
    exploration = tgt_noreuse_expl.explore()
    feedback = tgt_noreuse_kin.execute(exploration['m_signal'])
    tgt_noreuse_expl.receive(exploration, feedback)
    tgt_noreuse_explorations.append((exploration, feedback))

tgt_noreuse_dataset  = {'m_channels'  : tgt_noreuse_kin.m_channels,
                's_channels'  : tgt_noreuse_kin.s_channels,
                'explorations': tgt_noreuse_explorations}

tgt_noreuse_xs = [explo[1]['s_signal']['x'] for explo in tgt_noreuse_dataset['explorations']]
tgt_noreuse_ys = [explo[1]['s_signal']['y'] for explo in tgt_noreuse_dataset['explorations']]
for stop in stops:
    plotting.scatter(tgt_noreuse_xs[:stop], tgt_noreuse_ys[:stop], x_range=[-1, 1], y_range=[-1, 1], title='target no-reuse {}'.format(stop),
                     fill_alpha= 0.5, line_color=None, radius=2.0, radius_units='screen', tools='')

