from osbot_utils.testing.Temp_Folder import Temp_Folder
from osbot_utils.utils.Files import is_file, is_folder, files_recursive, filter_parent_folder, temp_file
from osbot_utils.utils.Zip import zip_files_to_bytes


class Temp_Zip_In_Memory:

    def __init__(self, targets=None):
        self.targets   = targets or []
        self.root_path = None

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        pass

    def add_file(self, file):
        if is_file(file):
            self.targets.append(file)
        return self

    def add_folder(self, folder):
        if type(folder) is Temp_Folder:
            folder = folder.path()
        if is_folder(folder):
            self.targets.append(folder)
        return self

    def all_source_files(self):
        all_files = []
        for target in self.targets:
            if is_file(target):
                all_files.append(target)
            elif is_folder(target):
                all_files.extend(files_recursive(target))
        return all_files

    def create_zip_file(self, target_zip_file=None):
        if target_zip_file is None:
            target_zip_file = temp_file(extension='.zip')
        with open(target_zip_file, 'wb') as f:
            f.write(self.zip_bytes())
        return target_zip_file

    def set_root_path(self, root_path):
        if type(root_path) is Temp_Folder:
            root_path = root_path.path()
        self.root_path = root_path
        return self

    def zip_bytes(self):
        return self.zip_buffer().getvalue()

    def zip_buffer(self):
        target_files = self.all_source_files()
        return zip_files_to_bytes(target_files, root_path=self.root_path)
