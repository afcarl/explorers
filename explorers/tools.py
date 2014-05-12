# -*- coding: utf-8 -*-
from __future__ import print_function, division
import importlib

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

def _load_class(classname):
    """Load a class from a string"""
    module_name, class_name = classname.rsplit('.', 1)
    module = importlib.import_module(module_name)
    return getattr(module, class_name)

def to_values(signal, channels=None):
    assert channels is None
    if isinstance(signal, collections.OrderedDict):
        return tuple(signal.values())
    else:
        # TODO dict with channels
        raise ValueError('Expected OrderedDict')

def to_signal(values, channels):
    return collections.OrderedDict((k, v) for k, v in zip(channels.keys(), values))
