import hashlib
import json
import os

GEAT_ROOT = '.geat_root'
GEAT_STACK = '.geat_stack'
GEAT_STAGE = '.geat_stage'


class GeatRoot:

    def __init__(self, directory='.', initialize=False):
        self.directory = directory
        self.real_root_path = os.path.realpath(self.directory)

        self._geat_root = os.path.join(self.real_root_path, GEAT_ROOT)
        self._geat_stack = os.path.join(self._geat_root, GEAT_STACK)
        self._geat_stage = os.path.join(self._geat_root, GEAT_STAGE)
        if not initialize and not self._check_geat_root_presence():
            self._check_geat_root_presence()
            # geat root not initialized or deleted
            raise Exception('There is no geat root here. Initialize geat')

    def _check_geat_root_presence(self):
        return os.path.isdir(self._geat_root)

    def initialize_root(self):
        try:
            os.mkdir(os.path.join(self.real_root_path, GEAT_ROOT))
            os.mkdir(os.path.join(self.real_root_path, GEAT_ROOT, GEAT_STACK))
            os.mkdir(os.path.join(self.real_root_path, GEAT_ROOT, GEAT_STAGE))
            print('Created.')
        except FileExistsError:
            print('Oops, looks like geat was already initialized.')
            raise Exception('Failed. Geat root already exists.')

    def add_file_to_geat_root(self, file_name):
        # for the first time, warn if file already added
        if not os.path.exists(os.path.join(self.real_root_path, file_name)):
            raise Exception(f'Error. File {file_name} does not exists.')
        hashed_file_name = hashlib.md5(file_name.encode()).hexdigest()
        if os.path.exists(os.path.join(self._geat_root, hashed_file_name)):
            print(
                f'Warning. '
                f'File {file_name} already in root as {hashed_file_name}'
            )
        else:
            self._create_new_geat_file_with_content(
                hashed_file_name, file_name
            )
            print(f'File {file_name} added as {hashed_file_name}')

    def _create_new_geat_file_with_content(self, hashed_file_name, file_name):
        source = os.path.join(self.real_root_path, file_name)
        destination = os.path.join(self._geat_stage, hashed_file_name)
        content = {}
        with open(source, 'r') as source_file:
            source_content = source_file.readlines()
        for line_no, line_content in enumerate(source_content, start=1):
            content[line_no] = line_content
        with open(destination, 'w') as file:
            file.write(json.dumps(content))
        print(f'Saved {file_name} as {hashed_file_name}.')
        print(f'Content {content}. \n...and done.')

    def status(self):
        stage = os.walk(self._geat_stage)
        print('staged files: ')
        for dir_path, dir_name, files in stage:
            for file in files:
                print(file)
        stack = os.walk(self._geat_stack)
        for dir_path, dir_name, files in stack:
            for file in files:
                print(file)

    def commit(self):
        stage = os.walk(self._geat_stage)
        for dir_path, dir_name, files in stage:
            for file in files:
                stage_path = os.path.join(self._geat_stage, file)
                stack_path = os.path.join(self._geat_stack, file)
                with open(stage_path, 'r') as staged_file:
                    buffer = staged_file.readlines()
                file_content = {}
                for line_number, line_content in enumerate(buffer, start=1):
                    file_content[line_number] = line_content
                with open(stack_path, 'w') as stacked_file:
                    stacked_file.write(json.dumps(file_content))
                os.remove(stage_path)
        print('committed')
