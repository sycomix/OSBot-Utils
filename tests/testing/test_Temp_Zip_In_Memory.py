from unittest import TestCase

from osbot_utils.utils.Files import file_exists, file_delete, file_extension

from osbot_utils.utils.Dev import pprint

from osbot_utils.testing.Temp_Folder import Temp_Folder
from osbot_utils.testing.Temp_Zip_In_Memory import Temp_Zip_In_Memory
from osbot_utils.utils.Zip import zip_files_to_bytes, zip_file_list


class test_Temp_Zip_In_Memory(TestCase):

    def test__with__default_params(self):
        with Temp_Zip_In_Memory() as _:
            assert _.targets == []

    def test_all_source_files(self):
        with Temp_Folder() as temp_folder:
            max_total_files = 30
            temp_folder.add_temp_files_and_folders(max_total_files=max_total_files)
            assert len(temp_folder.files()) == max_total_files
            with Temp_Zip_In_Memory() as temp_zip_in_memory:
                temp_zip_in_memory.add_folder(temp_folder)
                target_files_to_zip = temp_zip_in_memory.all_source_files()

                assert temp_folder.files(show_parent_folder=True) == target_files_to_zip
                assert len(temp_zip_in_memory.zip_bytes()) > 5000

    def test_create_zip_file(self):
        with Temp_Folder(temp_files_to_add=3) as temp_folder:
            with Temp_Zip_In_Memory() as _:
                _.add_folder(temp_folder)
                _.set_root_path(temp_folder)
                target_zip_file = _.create_zip_file()                           # save in memory zip into disk
                assert file_exists(target_zip_file)                             # make sure it exists
                assert file_extension(target_zip_file) == '.zip'                # make sure it has the right extension
                assert temp_folder.files() == zip_file_list(target_zip_file)    # confirm that all files inside temp_folder are inside the in memory zip file

        assert file_delete(target_zip_file) is True                             # delete the zip file

