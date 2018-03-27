import hashlib
import json
import os

GEAT_ROOT = '.geat_root'
GEAT_STACK = '.geat_stack'
GEAT_STAGE = '.geat_stage'
GEAT_DIFF = '.geat_diff'


class GeatRoot:

    def __init__(self, directory='.', initialize=False):
        self.directory = directory
        self.real_root_path = os.path.realpath(self.directory)

        self._geat_root = os.path.join(self.real_root_path, GEAT_ROOT)
        self._geat_stack = os.path.join(self._geat_root, GEAT_STACK)
        self._geat_stack_diff = os.path.join(self._geat_stack, GEAT_DIFF)
        self._geat_stage = os.path.join(self._geat_root, GEAT_STAGE)
        self._geat_stage_diff = os.path.join(self._geat_stage, GEAT_DIFF)
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
            os.mkdir(os.path.join(self.real_root_path, GEAT_ROOT, GEAT_STACK, GEAT_DIFF))
            os.mkdir(os.path.join(self.real_root_path, GEAT_ROOT, GEAT_STAGE))
            os.mkdir(os.path.join(self.real_root_path, GEAT_ROOT, GEAT_STAGE, GEAT_DIFF))
            print('Geat initialized.')
        except FileExistsError:
            print('Oops, looks like geat was already initialized.')

    def add_file_to_geat_root(self, file_name):
        if not os.path.exists(os.path.join(self.real_root_path, file_name)):
            raise Exception(f'Error. File {file_name} does not exists.')
        if os.path.exists(os.path.join(self._geat_stage, file_name)):
            print(f'Warning. File {file_name} already added.')
        else:
            self._create_new_geat_file_with_content(file_name)

    def _create_new_geat_file_with_content(self, file_name):
        source = os.path.join(self.real_root_path, file_name)
        destination = os.path.join(self._geat_stage, file_name)
        diff_destination = os.path.join(self._geat_stage_diff, file_name)
        content = {}
        with open(source, 'r') as source_file:
            source_content = source_file.readlines()
        for line_no, line_content in enumerate(source_content, start=1):
            content[line_no] = line_content
        # create hash value from file content
        hashed_content = hashlib.md5(json.dumps(content).encode()).hexdigest()
        with open(diff_destination, 'w') as diff_file:
            diff_file.write(hashed_content)
        with open(destination, 'w') as file:
            file.write(json.dumps(content))
        print(f'File {file_name} added to stage.')

    def status(self):
        stage_state = {}
        stack_state = {}
        diff_state = {}

        stage = os.walk(self._geat_stage)
        for dir_path, dir_name, files in stage:
            for file in files:
                hashed_content_value = self._get_hashed_content(
                    os.path.join(dir_path, file)
                )
                stage_state[file] = hashed_content_value

        stack = os.walk(self._geat_stack)
        for dir_path, dir_name, files in stack:

            for file in files:
                hashed_content_value = self._get_hashed_content(
                    os.path.join(dir_path, file)
                )
                stack_state[file] = hashed_content_value

        diff = os.walk(self._geat_stack_diff)
        for dir_path, dir_name, files in diff:
            for file in files:
                hashed_content_value = self._get_hashed_content(
                    os.path.join(dir_path, file)
                )
                diff_state[file] = hashed_content_value

        print('SUMMARY:')
        print('\tSTAGE:')
        for file, state in stage_state.items():
            this_file_diff = stack_state.get(file)
            if not this_file_diff:
                print(f'\t\tAdded to staging. File: {file}')
            elif state != this_file_diff:
                print(f'\t\tFILE: {file} got changed.')
            else:
                pass
        print('\tSTACK:')
        for file, state in stack_state.items():
            this_file_diff = diff_state.get(file)
            if not this_file_diff:
                print(f'\t\tEmpty history for file {file}')
                continue
            elif state != this_file_diff:
                print(f'\t\tFILE: {file} got changed.')
            else:
                pass

    def commit(self):
        stage = os.walk(self._geat_stage)
        for dir_path, dir_name, files in stage:
            for file in files:
                stage_path = os.path.join(self._geat_stage, file)
                stage_diff_path = os.path.join(self._geat_stage_diff, file)
                stack_path = os.path.join(self._geat_stack, file)
                diff_path = os.path.join(self._geat_stack_diff, file)
                with open(stage_path, 'r') as staged_file:
                    buffer = staged_file.readlines()
                file_content = {}
                for line_number, line_content in enumerate(buffer, start=1):
                    file_content[line_number] = line_content
                hashed_content = hashlib.md5(json.dumps(file_content).encode()).hexdigest()
                with open(diff_path, 'w') as diff_file:
                    diff_file.write(hashed_content)
                with open(stack_path, 'w') as stacked_file:
                    stacked_file.write(json.dumps(file_content))
                os.remove(stage_path)
                os.remove(stage_diff_path)

        print('Changes committed')

    @staticmethod
    def _get_hashed_content(source):
        content = {}
        with open(source, 'r') as source_file:
            source_content = source_file.readlines()
        for line_no, line_content in enumerate(source_content, start=1):
            content[line_no] = line_content
        return hashlib.md5(json.dumps(content).encode()).hexdigest()
