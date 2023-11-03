import gzip

import os
import glob
import pickle
import re
import shutil
import tempfile
from   os.path              import abspath, join
from pathlib import Path, PosixPath
from osbot_utils.utils.Misc import bytes_to_base64, base64_to_bytes, random_string


class Files:
    @staticmethod
    def bytes(path):
        with open(path, 'rb') as file:
            return file.read()

    @staticmethod
    def copy(source:str, destination:str) -> str:
        if file_exists(source):                                     # make sure source file exists
            destination_parent_folder = parent_folder(destination)  # get target parent folder
            folder_create(destination_parent_folder)                # ensure targer folder exists       # todo: check if this is still needed (we should be using a copy method that creates the required fodlers)
            return shutil.copy(source, destination)                 # copy file and returns file destination

    @staticmethod
    def contains(path, content):
        text = Files.contents(path)
        if type(content) is list:
            return all(item in text for item in content)
        return content in text

    @staticmethod
    def contents(path, mode='rt'):
        if file_exists(path):
            with file_open(path, mode) as file:
                return file.read()

    @staticmethod
    def contents_gz(path, mode='rt'):
        if file_exists(path):
            with file_open_gz(path, mode) as file:
                return file.read()

    @staticmethod
    def contents_md5(path):
        from osbot_utils.utils.Misc import bytes_md5
        return bytes_md5(file_contents_as_bytes(path))

    @staticmethod
    def contents_sha256(path):
        from osbot_utils.utils.Misc import bytes_sha256
        return bytes_sha256(file_contents_as_bytes(path))

    @staticmethod
    def current_folder():
        return Files.path_combine(".","")

    @staticmethod
    def delete(path):
        if Files.exists(path):
            os.remove(path)
            return Files.exists(path) is False
        return False

    @staticmethod
    def exists(path):
        return is_file(path)
        # if path and is_file(path):
        #     return os.path.exists(path)
        # return False

    @staticmethod
    def find(path_pattern, recursive=True):
        return glob.glob(path_pattern, recursive=recursive)

    @staticmethod
    def files(path, pattern= '*.*'):                        # todo: check behaviour and improve ability to detect file (vs folders)
        result = [str(file) for file in Path(path).rglob(pattern)]
        return sorted(result)

    @staticmethod
    def files_names(files : list):
        return [file_name(file) for file in files if is_file(file)]

    @staticmethod
    def file_create_all_parent_folders(file_path):
        if file_path:
            if parent_path := parent_folder(file_path):
                path        = Path(parent_path)
                path.mkdir(parents=True, exist_ok=True)
                return parent_path

    @staticmethod
    def file_name(path, check_if_exists=True):
        if is_file(path) or check_if_exists is False:
            return os.path.basename(path)

    @staticmethod
    def file_extension(path):
        return os.path.splitext(path)[1] if path else ''

    @staticmethod
    def file_extension_fix(extension):
        if extension is None or len(extension) == 0:        # if it None or empty return default .tmp extension
            return '.tmp'
        return f'.{extension}' if extension[0] != '.' else extension

    @staticmethod
    def file_to_base64(path):
        return bytes_to_base64(file_bytes(path))

    @staticmethod
    def file_from_base64(bytes_base64, path=None, extension=None):
        bytes_ = base64_to_bytes(bytes_base64)
        return file_create_bytes(bytes=bytes_, path=path, extension=None)

    @staticmethod
    def file_size(path):
        return file_stats(path).st_size

    @staticmethod
    def file_stats(path):
        return os.stat(path)

    @staticmethod
    def filter_parent_folder(items, folder):
        all_relative_items = [item.replace(folder, '')[1:] for item in items]
        return sorted(all_relative_items)

    @staticmethod
    def files_recursive(parent_dir, include_folders=False):
        all_files = []
        if os.path.isdir(parent_dir):
            for item in os.listdir(parent_dir):
                item_path = os.path.join(parent_dir, item)
                if os.path.isfile(item_path):
                    all_files.append(item_path)
                elif os.path.isdir(item_path):
                    if include_folders:
                        all_files.append(f'{item_path}/')
                    all_files.extend(files_recursive(item_path,include_folders=include_folders))


        return sorted(all_files)


    @staticmethod
    def folder_exists(path):
        return is_folder(path)

    @staticmethod
    def folder_copy(source, destination, ignore_pattern=None):
        if ignore_pattern:
            if type(ignore_pattern) is str:
                ignore_pattern = [ignore_pattern]
            ignore = shutil.ignore_patterns(*ignore_pattern)            # for example ignore_pattern = ['*.pyc','.DS_Store']
        else:
            ignore = None
        return shutil.copytree(src=source, dst=destination, ignore=ignore)

    @staticmethod
    def folder_create(path):
        if folder_exists(path):
            return path

        os.makedirs(path)
        return path

    @staticmethod
    def folder_create_in_parent(path, name):
        folder_path = path_combine(path, name)
        return folder_create(folder_path)

    @staticmethod
    def folder_delete(target_folder):
        if folder_exists(target_folder):
            try:
                os.rmdir(target_folder)
                return True
            except OSError:
                pass
        return False

    @staticmethod
    def folder_delete_all(path):                # this will remove recursively
        if folder_exists(path):
            shutil.rmtree(path)
            return folder_exists(path) is False
        return False

    @staticmethod
    def folder_name(path):
        if path:
            return os.path.basename(path)

    @staticmethod
    def folder_not_exists(path):
        return folder_exists(path) is False

    @staticmethod
    def folder_sub_folders(path):
        result = []
        item: os.DirEntry
        if Files.is_folder(path):
            result.extend(item.path for item in os.scandir(path) if item.is_dir())
        return result

    @staticmethod
    def folders_names(folders : list):
        result = [folder_name(folder) for folder in folders if folder]
        return sorted(result)

    @staticmethod
    def folders_sub_folders(folders : list):
        result = []
        for folder in folders:
            result.extend(Files.folder_sub_folders(folder))
        return result

    @staticmethod
    def folders_recursive(parent_dir):
        subdirectories = []
        for item in os.listdir(parent_dir):
            item_path = os.path.join(parent_dir, item)
            if os.path.isdir(item_path):
                subdirectories.append(item_path)
                subdirectories.extend(folders_recursive(item_path))

        return sorted(subdirectories)


    @staticmethod
    def is_file(target):
        if isinstance(target, Path):
            return target.is_file()
        return os.path.isfile(target) if type(target) is str else False

    @staticmethod
    def is_folder(target):
        if isinstance(target, Path):
            return target.is_dir()
        return os.path.isdir(target) if type(target) is str else False

    @staticmethod
    def lines(path):
        with open(path, "rt") as file:
            yield from file

    @staticmethod
    def lines_gz(path):
        with gzip.open(path, "rt") as file:
            yield from file

    @staticmethod
    def not_exists(path):
        return os.path.exists(path) is False

    @staticmethod
    def open(path, mode='r'):
        return open(path, mode=mode)

    @staticmethod
    def open_gz(path, mode='r'):
        return gzip.open(path, mode=mode)

    @staticmethod
    def open_bytes(path):
        return Files.open(path, mode='rb')

    @staticmethod
    def path_combine(path1, path2):
        if type(path1) in [str, Path] and type(path2) in [str, Path]:
            return abspath(join(str(path1), str(path2)))

    @staticmethod
    def parent_folder(path):
        if path:
            return os.path.dirname(path)

    @staticmethod
    def parent_folder_combine(file, path):
        return Files.path_combine(os.path.dirname(file),path)

    @staticmethod
    def pickle_save_to_file(object_to_save, path=None):
        path = path or temp_file(extension=".pickle")
        with open(path, "wb") as file_to_store:
            pickle.dump(object_to_save, file_to_store)
        return path

    @staticmethod
    def pickle_load_from_file(path=None):
        with open(path, "rb") as file_to_read:
            loaded_object = pickle.load(file_to_read)
        return loaded_object

    @staticmethod
    def safe_file_name(file_name):
        if type(file_name) is not str:
            file_name = f"{file_name}"
        return re.sub(r'[^a-zA-Z0-9_.]', '_',file_name or '')

    @staticmethod
    def save(contents, path=None, extension=None):
        path = path or temp_file(extension=extension)
        file_create(path, contents)
        return path

    @staticmethod
    def sub_folders(target):
        if type(target) is list:
            return Files.folders_sub_folders(target)
        return Files.folder_sub_folders(target) if type(target) is str else []

    @staticmethod
    def save_bytes_as_file(bytes_to_save, path=None, extension=None):
        if path is None:
            path = Files.temp_file(extension)
        with open(path, 'wb') as fp:
            fp.write(bytes_to_save)
        return path

    @staticmethod
    def temp_file(extension = '.tmp', contents=None, target_folder=None):
        extension = file_extension_fix(extension)
        if target_folder is None:
            (fd, tmp_file) = tempfile.mkstemp(extension)
            file_delete(tmp_file)
        else:
            tmp_file = path_combine(target_folder, temp_filename(extension))

        if contents:
            file_create(tmp_file, contents)
        return tmp_file

    @staticmethod
    def temp_file_in_folder(target_folder, prefix="temp_file_", postfix='.txt'):
        if is_folder(target_folder):
            path_to_file = path_combine(target_folder, random_string(prefix=prefix, postfix=postfix))
            file_create(path_to_file, random_string())
            return path_to_file

        

    @staticmethod
    def temp_filename(extension='.tmp'):
        return file_name(temp_file(extension), check_if_exists=False)

    @staticmethod
    def temp_folder(prefix=None, suffix=None,target_folder=None):
        return tempfile.mkdtemp(suffix, prefix, target_folder)

    @staticmethod
    def temp_folder_current():
        return tempfile.gettempdir()

    @staticmethod
    def temp_folder_with_temp_file(prefix=None, suffix=None,parent_folder=None, file_name='temp_file.txt', file_contents='temp_file'):
        folder = temp_folder(prefix,suffix,parent_folder)
        file_create(path_combine(folder,file_name), file_contents)
        return folder

    @staticmethod
    def write(path = None,contents=None, extension=None, mode='w'):
        path     = path or temp_file(extension)
        contents = contents or ''
        with open(file=path, mode=mode) as file:
            file.write(contents)
        return path

    @staticmethod
    def write_bytes(path=None, bytes=None, extension=None):
        return Files.write(path=path, contents=bytes, extension=extension, mode='wb')

    @staticmethod
    def write_gz(path=None, contents=None):
        path = path or temp_file(extension='.gz')
        contents = contents or ''
        if type(contents) is str:
            contents = contents.encode()
        with gzip.open(path, "w") as file:
            file.write(contents)
        return path




# helper methods
# todo: all all methods above (including the duplicated mappings at the top)

create_folder                  = Files.folder_create
create_folder_in_parent        = Files.folder_create_in_parent
create_temp_file               = Files.write
current_folder                 = Files.current_folder
current_temp_folder            = Files.temp_folder_current

file_bytes                     = Files.bytes
file_contains                  = Files.contains
file_contents                  = Files.contents
file_contents_gz               = Files.contents_gz
file_contents_md5              = Files.contents_md5
file_contents_sha256           = Files.contents_sha256
file_contents_as_bytes         = Files.bytes
file_create_all_parent_folders = Files.file_create_all_parent_folders
file_copy                      = Files.copy
file_delete                    = Files.delete
file_create                    = Files.write
file_create_bytes              = Files.write_bytes
file_create_from_bytes         = Files.write_bytes
file_create_gz                 = Files.write_gz
file_exists                    = Files.exists
file_extension                 = Files.file_extension
file_extension_fix             = Files.file_extension_fix
file_lines                     = Files.lines
file_lines_gz                  = Files.lines_gz
file_md5                       = Files.contents_md5
file_name                      = Files.file_name
file_not_exists                = Files.not_exists
file_open                      = Files.open
file_open_gz                   = Files.open_gz
file_open_bytes                = Files.open_bytes
file_to_base64                 = Files.file_to_base64
file_from_base64               = Files.file_from_base64
file_save                      = Files.save
file_sha256                    = Files.contents_sha256
file_size                      = Files.file_size
file_stats                     = Files.file_stats
file_write                     = Files.write
file_write_bytes               = Files.write_bytes
file_write_gz                  = Files.write_gz
filter_parent_folder           = Files.filter_parent_folder
files_find                     = Files.find
files_recursive                = Files.files_recursive
files_list                     = Files.files
files_names                    = Files.files_names

find_files                     = Files.files

folder_create                  = Files.folder_create
folder_create_in_parent        = Files.folder_create_in_parent
folder_create_temp             = Files.temp_folder
folder_copy                    = Files.folder_copy
folder_copy_except             = Files.folder_copy
folder_delete                  = Files.folder_delete
folder_delete_all              = Files.folder_delete_all
folder_delete_recursively      = Files.folder_delete_all
folder_exists                  = Files.folder_exists
folder_not_exists              = Files.folder_not_exists
folder_name                    = Files.folder_name
folder_temp                    = Files.temp_folder
folder_files                   = Files.files
folder_sub_folders             = Files.folder_sub_folders

folders_in_folder              = Files.folder_sub_folders
folders_names                  = Files.folders_names
folders_recursive              = Files.folders_recursive
folders_sub_folders            = Files.folders_sub_folders

is_file                     = Files.is_file
is_folder                   = Files.is_folder

load_file                   = Files.contents
load_file_gz                = Files.contents_gz

path_append                 = Files.path_combine
path_combine                = Files.path_combine
path_current                = Files.current_folder
parent_folder               = Files.parent_folder
parent_folder_combine       = Files.parent_folder_combine
pickle_load_from_file       = Files.pickle_load_from_file
pickle_save_to_file         = Files.pickle_save_to_file

safe_file_name              = Files.safe_file_name
save_bytes_as_file          = Files.save_bytes_as_file
save_string_as_file         = Files.save
sub_folders                 = Files.sub_folders

temp_file                   = Files.temp_file
temp_file_in_folder         = Files.temp_file_in_folder
temp_filename               = Files.temp_filename
temp_folder                 = Files.temp_folder
temp_folder_current         = Files.temp_folder_current
temp_folder_with_temp_file  = Files.temp_folder_with_temp_file

