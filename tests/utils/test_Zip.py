from unittest import TestCase

from osbot_utils.utils.Misc import random_string

from osbot_utils.utils.Files import file_contents, folder_files, temp_folder_with_temp_file, file_exists, \
    file_extension
from osbot_utils.utils.Zip import zip_file_list, unzip_file, folder_zip


class test_Zip(TestCase):

    def test_folder_zip(self):
        folder = temp_folder_with_temp_file(file_contents=random_string())
        print()

        zip_file = folder_zip(folder)

        assert file_exists   (zip_file) is True
        assert file_extension(zip_file) == '.zip'

        unziped_folder = unzip_file(zip_file)

        source_files  = folder_files(folder)
        target_files  = folder_files(unziped_folder)

        assert len(source_files) == 1
        assert len(target_files) == 1
        assert source_files[0]   != target_files[0]

        assert file_contents(source_files[0]) == file_contents(target_files[0])

        assert zip_file_list(zip_file)        == ['temp_file.txt']