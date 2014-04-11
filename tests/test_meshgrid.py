from __future__ import absolute_import, division, print_function
import unittest
import random

import dotdot
from explorer.explorers import reuse


random.seed(0)


class TestMeshGrid(unittest.TestCase):

    def test_meshgrid1D(self):
        mesh = reuse.MeshGrid(((0, 1),), 10)
        for _ in range(10000):
            mesh.add((random.random(),))

        self.assertEqual(len(mesh._nonempty_bins), 10)

        mesh2 = reuse.MeshGrid(((0, 1),), 10)
        for _ in range(1000):
            mesh2.add(mesh.draw(replace=True))

        for b in mesh2._nonempty_bins:
            self.assertTrue(80 <= len(b) <= 120)

        mesh3 = reuse.MeshGrid(((0, 1),), 10)
        for _ in range(1000):
            mesh3.add(mesh.draw(replace=False))

        for b in mesh3._nonempty_bins:
            self.assertTrue(80 <= len(b) <= 120)

        self.assertEqual(len(mesh._nonempty_bins), 10)

    def test_meshgrid2D(self):
        bounds = ((-30, -20), (4, 5))
        res = 15

        mesh = reuse.MeshGrid(bounds, res)
        for _ in range(10000):
            mesh.add((random.uniform(*bounds[0]),
                      random.uniform(*bounds[1])))

        self.assertEqual(len(mesh._nonempty_bins), res**2)

        res2 = 10
        mesh2 = reuse.MeshGrid(bounds, res2)
        for _ in range(1000):
            mesh2.add(mesh.draw(replace=True))

        self.assertEqual(len(mesh2._nonempty_bins), res2**2)

    def test_meshgrid_outliers(self):
        bounds = ((0, 1),)
        res = 15

        mesh = reuse.MeshGrid(bounds, res)
        for _ in range(1000):
            mesh.add(( random.uniform(*bounds[0]),))
        for _ in range(1000):
            mesh.add((-random.uniform(*bounds[0]),))

        self.assertEqual(len(mesh._nonempty_bins), res+1)

        res2 = 10
        mesh2 = reuse.MeshGrid(bounds, res2)
        for _ in range(100):
            mesh2.add(mesh.draw(replace=True))

        for b in mesh2._nonempty_bins:
            self.assertTrue(3 < len(b) < 20)
        self.assertEqual(len(mesh2._nonempty_bins), res2+1)

if __name__ == '__main__':
    unittest.main()
