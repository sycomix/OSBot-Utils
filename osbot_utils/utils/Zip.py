import io
import os
import shutil
import zipfile
from os.path import abspath

from osbot_utils.utils.Files import temp_folder, folder_files, temp_file, is_file


def unzip_file(zip_file, target_folder=None, format='zip'):
    target_folder = target_folder or temp_folder()
    shutil.unpack_archive(zip_file, extract_dir=target_folder, format=format)
    return target_folder

def zip_files_to_bytes(file_paths, root_path=None):
    zip_buffer = io.BytesIO()                                                   # Create a BytesIO buffer to hold the zipped file
    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zf:          # Create a ZipFile object with the buffer as the target
        for file_path in file_paths:
            if root_path:
                arcname = file_path.replace(root_path,'')                       # Define the arcname, which is the name inside the zip file
            else:
                arcname = file_path                                             # if root_path is not provided, use the full file path
            zf.write(file_path, arcname)                                        # Add the file to the zip file
    zip_buffer.seek(0)
    return zip_buffer

def zip_folder(root_dir, format='zip'):
    return shutil.make_archive(base_name=root_dir, format=format, root_dir=root_dir)

def zip_folder_to_bytes(root_dir):      # todo add unit test
    zip_buffer = io.BytesIO()                                                   # Create a BytesIO buffer to hold the zipped file
    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zf:          # Create a ZipFile object with the buffer as the target
        for foldername, subfolders, filenames in os.walk(root_dir):             # Walk the root_dir and add all files and folders to the zip file
            for filename in filenames:
                absolute_path = os.path.join(foldername, filename)              # Create the complete filepath
                arcname = os.path.relpath(absolute_path, root_dir)              # Define the arcname, which is the name inside the zip file
                zf.write(absolute_path, arcname)                                # Add the file to the zip file
    zip_buffer.seek(0)                                                          # Reset buffer position
    return zip_buffer

def zip_file_list(path):
    if is_file(path):
        with zipfile.ZipFile(path) as zip_file:
            return sorted(zip_file.namelist())
    return []

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


# extra function's mappings
file_unzip  = unzip_file
folder_zip  = zip_folder