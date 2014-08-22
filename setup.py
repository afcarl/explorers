import os
from distutils.core import setup

setup(
    name = "explorers",
    version = "0.2",
    author = "Fabien Benureau",
    author_email = "fabien.benureau@inria.fr",
    description = ("Framework for exploration algorithms"),
    license = "Open Science.",
    keywords = "exploration learning algorithm",
    url = "flowers.inria.fr",
    packages=['explorers',
              'explorers.algorithms',
              'explorers.algorithms.reuse',
              'explorers.algorithms.im',
                          ],
    requires=['leaners'],
    classifiers=[],
)
