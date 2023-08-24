from osbot_utils.utils.Misc import random_string

from osbot_utils.utils.Files import path_combine, temp_folder_current, safe_file_name, folder_exists, folder_create, \
    folder_delete_recursively, zip_folder, files_list, file_create


class Temp_Folder:

    def __init__(self, folder_name=None, temp_prefix=None, delete_on_exit=True):
        self.folder_name         = folder_name or f"temp_folder_{temp_prefix}_{random_string()}"
        self.current_temp_folder = temp_folder_current()
        self.temp_folder         = path_combine(self.current_temp_folder, safe_file_name(self.folder_name))
        self.delete_on_exit      = delete_on_exit


    def __enter__(self):
        folder_create(self.temp_folder)
        return self

    def __exit__(self, type, value, traceback):
        if self.delete_on_exit:
            folder_delete_recursively(self.temp_folder)

    def add_file(self, file_name, contents):
        file_path = path_combine(self.temp_folder, safe_file_name(file_name))
        return file_create(file_path, contents)

    def add_folder(self, name):
        new_folder = path_combine(self.path(), safe_file_name(name))
        return folder_create(new_folder)

    def exists(self):
        return folder_exists(self.temp_folder)

    def path(self):
        return self.temp_folder

    def files(self):
        return files_list(self.path())

    def zip(self):
        return zip_folder(self.path())