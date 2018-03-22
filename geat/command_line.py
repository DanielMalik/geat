import os
import sys

from geat.core import GeatRoot


def initialize():
    geat = GeatRoot(initialize=True)
    geat.initialize_root()


def add_file():
    geat = GeatRoot()
    file_name = sys.argv[1]
    if file_name in ['*', 'all']:
        files = os.walk(os.path.realpath('.'))
        for dir_path, dir_names, files in files:
            for file in files:
                geat.add_file_to_geat_root(file)
    else:
        geat.add_file_to_geat_root(file_name)


def get_status():
    geat = GeatRoot()
    geat.status()


def commit_to_stack():
    geat = GeatRoot()
    geat.commit()
