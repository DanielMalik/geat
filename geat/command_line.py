import sys

from geat.die_tryin import DieTryin
from geat.core import GeatRoot


def main():
    shot = DieTryin()
    shot.run()


def initialize():
    geat = GeatRoot(initialize=True)
    geat.initialize_root()


def add_file():
    file_name = sys.argv[1]
    geat = GeatRoot()
    geat.add_file_to_geat_root(file_name)
