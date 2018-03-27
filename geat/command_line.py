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
                if '.' not in dir_path:
                    print(os.path.join(dir_path, file))
                    geat.add_file_to_geat_root(file)
    else:
        geat.add_file_to_geat_root(file_name)


def get_status():
    geat = GeatRoot()
    geat.status()


def commit_to_stack():
    geat = GeatRoot()
    geat.commit()


def handle_geat_command():
    command = sys.argv[1]
    if command == 'init':
        geat = GeatRoot(initialize=True)
        geat.initialize_root()
    else:
        geat = GeatRoot()
        if command == 'add':
            try:
                file_name = sys.argv[2]
            except IndexError:
                raise Exception('Specify files. Type "all" to add all.')
            print('filename in command = ', file_name)
            if file_name == 'all':
                files = os.walk(os.path.realpath('.'))
                for dir_path, dir_names, files in files:
                    if '.' not in dir_path:
                        for file in files:
                            geat.add_file_to_geat_root(file)
            else:
                geat.add_file_to_geat_root(file_name)

        elif command == 'status':
            geat.status()
        elif command == 'commit':
            geat.commit()
        else:
            print(f'GEAT Error. Unknown command: {command}')
