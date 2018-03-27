import os
import sys

from geat.core import GeatRoot


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
