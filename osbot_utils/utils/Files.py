import gzip
import os
import glob
import shutil
import tempfile
import zipfile
from   os.path import abspath, join

# todo: add UnitTests to methods below (and refactor these to use the methods in the Files class (so that we don't have duplicated code)
from pathlib import Path

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
    def contents(path):
        with open(path, "rt") as file:
            return file.read()

    @staticmethod
    def contents_gz(path):
        with gzip.open(path, "rt") as file:
            return file.read()

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
    def file_size(path):
        return file_stats(path).st_size

    @staticmethod
    def file_stats(path):
        return os.stat(path)

    @staticmethod
    def folder_exists(path):          # todo: add check to see if it is a folder
        return Files.exists(path)

    staticmethod
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
    def path_combine(path1, path2):
        return abspath(join(path1, path2))

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
    def open_bytes(path):
        return Files.open(path, mode='rb')

    @staticmethod
    def parent_folder(path):
        return os.path.dirname(path)

    @staticmethod
    def parent_folder_combine(file, path):
        return Files.path_combine(os.path.dirname(file),path)

    @staticmethod
    def save(contents, path=None, extension=None):
        path = path or temp_file(extension=extension)
        file_create(path, contents)
        return path


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
    def write_bytes(path=None, contents=None, extension=None):
        return Files.write(path=path, contents=contents, extension=extension, mode='wb')

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

current_folder              = Files.current_folder

file_bytes                  = Files.bytes
file_contents               = Files.contents
file_contents_gz            = Files.contents_gz
file_contents_as_bytes      = Files.bytes
file_copy                   = Files.copy
file_delete                 = Files.delete
file_create                 = Files.write
file_create_bytes           = Files.write_bytes
file_create_gz              = Files.write_gz
file_exists                 = Files.exists
file_extension              = Files.file_extension
file_extension_fix          = Files.file_extension_fix
file_find                   = Files.find
file_lines                  = Files.lines
file_lines_gz               = Files.lines_gz
file_name                   = Files.file_name
file_not_exists             = Files.not_exists
file_open                   = Files.open
file_open_bytes             = Files.open_bytes
file_save                   = Files.save
file_size                   = Files.file_size
file_stats                  = Files.file_stats
file_write                  = Files.write
file_write_bytes            = Files.write_bytes
file_write_gz               = Files.write_gz
file_unzip                  = Files.unzip_file

folder_create               = Files.folder_create
folder_create_temp          = Files.temp_folder
folder_copy                 = Files.folder_copy
folder_copy_except          = Files.folder_copy
folder_delete_all           = Files.folder_delete_all
folder_exists               = Files.folder_exists
folder_not_exists           = Files.folder_not_exists
folder_name                 = Files.folder_name
folder_temp                 = Files.temp_folder
folder_files                = Files.files
folder_zip                  = Files.zip_folder

path_append                 = Files.path_combine
path_combine                = Files.path_combine
path_current                = Files.current_folder
parent_folder               = Files.parent_folder
parent_folder_combine       = Files.parent_folder_combine

save_bytes_as_file          = Files.save_bytes_as_file
save_string_as_file         = Files.save

temp_file                   = Files.temp_file
temp_filename               = Files.temp_filename
temp_folder                 = Files.temp_folder
temp_folder_with_temp_file  = Files.temp_folder_with_temp_file

zip_files                   = Files.zip_files
zip_folder                  = Files.zip_folder
zip_file_list               = Files.zip_file_list
unzip_file                  = Files.unzip_file