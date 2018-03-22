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
            'geat_init=geat.command_line:initialize',
            'geat_add=geat.command_line:add_file',
            'geat_status=geat.command_line:get_status',
            'geat_commit=geat.command_line:commit_to_stack',
        ],
    }
)
