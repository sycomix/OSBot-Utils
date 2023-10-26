from osbot_utils.utils.Misc import random_string

from osbot_utils.utils.Files import path_combine, temp_folder_current, safe_file_name, folder_exists, folder_create, \
    folder_delete_recursively, files_list, file_create, folder_files, folders_recursive, files_find, files_recursive
from osbot_utils.utils.Zip import zip_folder


class Temp_Folder:

    def __init__(self, folder_name=None, parent_folder=None, temp_prefix=None, delete_on_exit=True):
        if type(parent_folder) is Temp_Folder:
            parent_folder = parent_folder.path()
        self.folder_name         = folder_name or f"temp_folder_{random_string(prefix=temp_prefix)}"
        self.parent_folder       = parent_folder or temp_folder_current()
        self.full_path           = path_combine(self.parent_folder, safe_file_name(self.folder_name))
        self.delete_on_exit      = delete_on_exit


    def __enter__(self):
        folder_create(self.full_path)
        return self

    def __exit__(self, type, value, traceback):
        if self.delete_on_exit:
            folder_delete_recursively(self.full_path)

    def add_file(self, file_name=None, contents=None):
        if file_name is None: file_name = f"temp_file_{random_string()}.txt"
        if contents  is None: contents  = random_string()
        file_path = path_combine(self.full_path, safe_file_name(file_name))
        return file_create(file_path, contents)

    def add_folder(self, name=None):
        if name is None: name = f"temp_folder_{random_string()}"
        new_folder = path_combine(self.path(), safe_file_name(name))
        return folder_create(new_folder)

    def exists(self):
        return folder_exists(self.full_path)

    def path(self):
        return self.full_path

    def files(self, show_parent_folder=False, include_folders=False):
        all_files = files_recursive(self.path(), include_folders=include_folders)
        return self.filter_parent_folder(all_files, show_parent_folder)

    def files_and_folders(self, show_parent_folder=False):
        all_files   = files_find(self.path())
        all_folders = folders_recursive(self.path())

        return self.filter_parent_folder(all_files, show_parent_folder)

    def filter_parent_folder(self, items, show_parent_folder):
        if show_parent_folder:
            return items
        all_relative_items = []
        for item in items:
            all_relative_items.append(item.replace(self.path(),'')[1:])
        return all_relative_items

    def folders(self, show_parent_folder=False):
        all_folders = folders_recursive(self.path())
        return self.filter_parent_folder(all_folders, show_parent_folder)

    def zip(self):
        return zip_folder(self.path())