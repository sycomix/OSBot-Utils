import gzip
import os
import glob
import pickle
import re
import shutil
import tempfile
import zipfile
from   os.path import abspath, join
from pathlib import Path

from osbot_utils.utils.Misc import bytes_to_base64, base64_to_bytes


class Files:
    @staticmethod
    def bytes(path):
        with open(path, 'rb') as file:
            return file.read()

    @staticmethod
    def copy(source:str, destination:str) -> str:
        if file_exists(source):                                     # make sure source file exists
            parent_folder = Files.folder_name(destination)          # get target parent folder
            folder_create(parent_folder)                            # ensure targer folder exists
            return shutil.copy(source, destination)                 # copy file and returns file destination

    @staticmethod
    def contains(path, content):
        text = Files.contents(path)
        if type(content) is list:
            for item in content:
                if item not in text:
                    return False
            return True
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

    @staticmethod
    def exists(path):                           # todo: add check to see if it is a file (vs being a folder)_
        if path:
            return os.path.exists(path)
        return False

    @staticmethod
    def find(path_pattern, recursive=True):
        return glob.glob(path_pattern, recursive=recursive)

    @staticmethod
    def files(path, pattern= '*.*'):                        # todo: check behaviour and improve ability to detect file (vs folders)
        result = []
        for file in Path(path).rglob(pattern):
            result.append(str(file))                        # todo: see if there is a better way to do this conversion to string
        return sorted(result)

    @staticmethod
    def file_create_all_parent_folders(file_path):
        parent_path = parent_folder(file_path)
        path = Path(parent_path)
        path.mkdir(parents=True, exist_ok=True)
        return parent_path

    @staticmethod
    def file_name(path):
        return os.path.basename(path)

    @staticmethod
    def file_extension(path):
        if path:
            return os.path.splitext(path)[1]
        return ''

    @staticmethod
    def file_extension_fix(extension):
        if extension is None or len(extension) == 0:        # if it None or empty return default .tmp extension
            return '.tmp'
        if extension[0] != '.':                             # make sure that the extension starts with a dot
            return '.' + extension
        return extension

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
    def folder_exists(path):          # todo: add check to see if it is a folder
        return Files.exists(path)

    @staticmethod
    def folder_copy(source, destination, ignore_pattern=None):
        if ignore_pattern:
            ignore = shutil.ignore_patterns(ignore_pattern)
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
    def folder_delete_all(path):                # this will remove recursively
        if folder_exists(path):
            shutil.rmtree(path)
        return folder_exists(path) is False

    @staticmethod
    def folder_name(path):
        return os.path.dirname(path)

    @staticmethod
    def folder_not_exists(path):
        return folder_exists(path) is False

    @staticmethod
    def folder_sub_folders(path):
        result = []
        item: os.DirEntry
        if Files.is_folder(path):
            for item in os.scandir(path):
                if item.is_dir():
                    result.append(item.path)
        return result

    @staticmethod
    def folders_names(folders : list):
        result = []
        for folder in folders:
            if Files.is_folder(folder):
                result.append(Files.file_name(folder))
        return result

    @staticmethod
    def folders_sub_folders(folders : list):
        result = []
        for folder in folders:
            result.extend(Files.folder_sub_folders(folder))
        return result

    @staticmethod
    def is_file(target):
        return os.path.isfile(target)

    @staticmethod
    def is_folder(target):
        return os.path.isdir(target)

    @staticmethod
    def lines(path):
        with open(path, "rt") as file:
            for line in file:
                yield line

    @staticmethod
    def lines_gz(path):
        with gzip.open(path, "rt") as file:
            for line in file:
                yield line

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
        return abspath(join(path1, path2))

    @staticmethod
    def parent_folder(path):
        return os.path.dirname(path)

    @staticmethod
    def parent_folder_combine(file, path):
        return Files.path_combine(os.path.dirname(file),path)

    @staticmethod
    def pickle_save_to_file(object_to_save, path=None):
        path = path or temp_file(extension=".pickle")
        file_to_store = open(path, "wb")
        pickle.dump(object_to_save, file_to_store)
        file_to_store.close()
        return path

    @staticmethod
    def pickle_load_from_file(path=None):
        file_to_read = open(path, "rb")
        loaded_object = pickle.load(file_to_read)
        file_to_read.close()
        return loaded_object

    @staticmethod
    def safe_file_name(file_name):
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
        if type(target) is str:
            return Files.folder_sub_folders(target)
        return []

    @staticmethod
    def save_bytes_as_file(bytes_to_save, path=None, extension=None):
        if path is None:
            path = Files.temp_file(extension)
        with open(path, 'wb') as fp:
            fp.write(bytes_to_save)
        return path

    @staticmethod
    def temp_file(extension = '.tmp', contents=None, parent_folder=None):
        extension = file_extension_fix(extension)
        if parent_folder is None:
            (fd, tmp_file) = tempfile.mkstemp(extension)
            file_delete(tmp_file)
        else:
            tmp_file = path_combine(parent_folder, temp_filename(extension))

        if contents:
            file_create(tmp_file, contents)
        return tmp_file

    @staticmethod
    def temp_filename(extension='.tmp'):
        return Files.file_name(Files.temp_file(extension))

    @staticmethod
    def temp_folder(prefix=None, suffix=None,parent_folder=None):
        return tempfile.mkdtemp(suffix, prefix, parent_folder)

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

    @staticmethod
    def unzip_file(zip_file, target_folder=None, format='zip'):
        target_folder = target_folder or temp_folder()
        shutil.unpack_archive(zip_file, extract_dir=target_folder, format=format)
        return target_folder

    @staticmethod
    def zip_folder(root_dir, format='zip'):
        return shutil.make_archive(base_name=root_dir, format=format, root_dir=root_dir)

    @staticmethod
    def zip_file_list(path):
        with zipfile.ZipFile(path) as zip_file:
            return sorted(zip_file.namelist())

    @staticmethod
    def zip_files(base_folder, file_pattern="*.*", target_file=None):
        base_folder = abspath(base_folder)
        file_list   = folder_files(base_folder, file_pattern)

        if len(file_list):                                                  # if there were files found
            target_file = target_file or temp_file(extension='zip')
            with zipfile.ZipFile(target_file,'w') as zip:
                for file_name in file_list:
                    zip_file_path = file_name.replace(base_folder,'')
                    zip.write(file_name, zip_file_path)

            return target_file



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
file_find                      = Files.find
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
file_unzip                     = Files.unzip_file
files_list                     = Files.files

folder_create                  = Files.folder_create
folder_create_in_parent        = Files.folder_create_in_parent
folder_create_temp             = Files.temp_folder
folder_copy                    = Files.folder_copy
folder_copy_except             = Files.folder_copy
folder_delete_all              = Files.folder_delete_all
folder_delete_recursively      = Files.folder_delete_all
folder_exists                  = Files.folder_exists
folder_not_exists              = Files.folder_not_exists
folder_name                    = Files.folder_name
folder_temp                    = Files.temp_folder
folder_files                   = Files.files
folder_zip                     = Files.zip_folder

folders_names               = Files.folders_names

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
temp_filename               = Files.temp_filename
temp_folder                 = Files.temp_folder
temp_folder_current         = Files.temp_folder_current
temp_folder_with_temp_file  = Files.temp_folder_with_temp_file

zip_files                   = Files.zip_files
zip_folder                  = Files.zip_folder
zip_file_list               = Files.zip_file_list
unzip_file                  = Files.unzip_file