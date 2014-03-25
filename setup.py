import os
from distutils.core import setup

setup(
    name = "explorer",
    version = "0.1",
    author = "Fabien Benureau",
    author_email = "fabien.benureau@inria.fr",
    description = ("Framework for exploration algorithms"),
    license = "Open Science.",
    keywords = "exploration learning algorithm",
    url = "flowers.inria.fr",
    packages=['explorer', 'explorer.env',
                          'explorer.explorers',
                          'explorer.learners',
                          ],
    classifiers=[],
)
