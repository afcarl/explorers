import os
from setuptools import setup

import versioneer

setup(
    name         = "explorers",
    version      = "1.0.2",
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
    dependency_links=[
        "https://github.com/flowersteam/forest/tarball/master#egg=forest-1.0",
    ],
    install_requires=['forest', 'learners', 'shapely'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Programming Language :: Python :: 2.7',
        'Intended Audience :: Science/Research',
    ]
)
