from __future__ import print_function, division

import numbers
import random

import numpy as np
import toolbox


class MeshBin(object):

    def __init__(self, coo, bounds=None):
        self.coo      = coo
        self.bounds   = bounds
        self.elements = []
        self.metadata = []

    def add(self, e, metadata=None):
        self.elements.append((e, metadata))

    def __len__(self):
        return len(self.elements)

    def draw(self, replace=True):
        idx = random.randint(0, len(self.elements) - 1)
        if replace:
            choice = self.elements[idx]
        else:
            choice = self.elements.pop(idx)
        return choice


class MeshGrid(object):
    """\
    Groups elements in bins and draw elements by choosing a bin at random.
    """

    def __init__(self, bounds, res):
        assert all(isinstance(b_min, numbers.Real) and
                   isinstance(b_max, numbers.Real) for b_min, b_max in bounds)
        self.bounds = bounds
        if isinstance(res, numbers.Integral):
            res = len(bounds)*[res]
        assert (len(res) == len(bounds) and
                all(isinstance(e, numbers.Integral) for e in res))
        self.res = res

        self.dim = len(bounds)
        self._bins = {}
        self._bins[None] = MeshBin(None) # a bin for everything not inside the bounds
        self._size = 0
        self._nonempty_bins = []

    def _coo(self, p):
        assert len(p) == self.dim
        coo = []
        for pi, (si_min, si_max), res_i in zip(p, self.bounds, self.res):
            coo.append(int((pi - si_min)/(si_max - si_min)*res_i))
            if pi == si_max:
                coo[-1] == res_i - 1
            if si_min > pi or si_max < pi:
                return None
        return tuple(coo)

    def __len__(self):
        return self._size

    def add(self, p, metadata=None):
        assert len(p) == self.dim
        self._size += 1
        coo = self._coo(p)
        if not coo in self._bins:
            self._bins[coo] = MeshBin(coo)
        bin = self._bins[coo]
        bin.add(p, metadata)
        if len(bin) == 1:
            self._nonempty_bins.append(bin)

    def draw(self, replace=True, metadata=False):
        """Draw uniformly between existing (non-empty) bins"""
        try:
            idx = random.randint(0, len(self._nonempty_bins) - 1)
        except ValueError:
            raise ValueError, "can't draw from an empty meshgrid"
        e, md = self._nonempty_bins[idx].draw(replace=replace)
        if len(self._nonempty_bins[idx]) == 0:
            self._nonempty_bins.pop(idx)
        if metadata:
            return e, md
        else:
            return e