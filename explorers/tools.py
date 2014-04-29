# -*- coding: utf-8 -*-
from __future__ import print_function, division

spac = '   '
down = '│  '
tndw = '├──'
turn = '└──'

def print_explorer(cfg):
    s = _explorers(cfg)
    return ''.join(s)

def _explorers(cfg, prefix=''):
    name = cfg.classname.rsplit('.', 1)[1]
    if name == 'Mix2Explorer':
        return _mix_explorer(cfg, prefix=prefix)
    else:
        return ['{}{}\n'.format(prefix, name)]

def _mix_explorer(cfg, prefix=''):
    s = ['{}Mix2\n'.format(prefix)]
    s.append('{}├── {}\n'.format(prefix, _timeline(cfg)))
    s.extend(_explorers(cfg.explorer_a, prefix=prefix+'│   '))
    s.append('{}└── else\n'.format(prefix))
    s.extend(_explorers(cfg.explorer_b, prefix=prefix+'    '))
    return s

def _timeline(cfg):
    if cfg.bootstrap_a > 0:
        if cfg.permitted_a < 1e308:
            return '100% (0-{}), then {}% until {}'.format(int(cfg.bootstrap_a), int(100*cfg.ratio_a), cfg.permitted_a)
        else:
            return '100% (0-{}), then {}%'.format(int(cfg.bootstrap_a), int(100*cfg.ratio_a))
    else:
        return '{}%'.format(int(100*cfg.ratio_a))
