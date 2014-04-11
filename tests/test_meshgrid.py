from __future__ import absolute_import, division, print_function
import unittest
import random

import forest

import dotdot
from explorer.explorers import reuse


random.seed(0)

class TestMeshGrid(unittest.TestCase):

    def test_randgexp(self):
        mesh = reuse.MeshGrid(((0, 1),), 10)
        for _ in range(100000):
            mesh.add((random.random(),))

        self.assertEqual(len(mesh._nonempty_bins), 10)

        mesh2 = reuse.MeshGrid(((0, 1),), 10)
        for _ in range(10000):
            mesh2.add(mesh.draw(replace=True))

        for b in mesh2._nonempty_bins:
            self.assertTrue(850 <= len(b) <= 1150)


if __name__ == '__main__':
    unittest.main()
