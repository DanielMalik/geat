#! /usr/bin/env python
# -----------------------------------------------------------------------------
# Copyright (c) 2018, NoLab Daniel Malik
#
# -----------------------------------------------------------------------------

from setuptools import setup

REQUIREMENTS = []


setup(
    name='geat',
    install_requires=REQUIREMENTS,
    python_requires='>=3.6',
    version='0.1',
    packages=['geat'],
    entry_points={
        'console_scripts': [
            'geat=geat.command_line:handle_geat_command',
        ],
    }
)
