import os
from setuptools import setup

import versioneer

setup(
    name         = "explorers",
    version      = "1.1.0",
    cmdclass     = versioneer.get_cmdclass(),
    author       = "Fabien Benureau",
    author_email = "fabien.benureau@inria.fr",
    description  = 'Framework for autonomous exploration algorithms in sensorimotor spaces',
    license      = "Open Science (see fabien.benureau.com/openscience.html",
    keywords     = "exploration learning algorithm sensorimotor robots robotics",
    url          = "github.com/humm/explorers.git",
    packages=[
        'explorers',
        'explorers.algorithms',
        'explorers.algorithms.reuse',
        'explorers.algorithms.im',
    ],
    install_requires=['numpy', 'scicfg', 'learners', 'shapely', 'environments'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Programming Language :: Python :: 2.7',
        'Intended Audience :: Science/Research',
    ]
)
