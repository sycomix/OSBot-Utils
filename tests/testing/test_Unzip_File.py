from unittest import TestCase

from osbot_utils.testing.Unzip_File import Unzip_File
from osbot_utils.testing.Zip_Folder import Zip_Folder
from osbot_utils.utils.Files import Files, parent_folder



class test_Unzip_File(TestCase):

    def test__using_with__no_params(self):
        with Unzip_File() as (temp_Folder):
            assert temp_Folder is None

    def test__using_with_valid_zip_no_target_folder(self):
        test_zip = parent_folder(__file__)
        with Zip_Folder(test_zip) as (zip_file):
            with Unzip_File(zip_file,None,True) as temp_folder:
                assert Files.exists(temp_folder) is True
        assert Files.exists(temp_folder) is False

    def test__using_with_valid_zip_and_target_folder(self):
        test_zip = parent_folder(__file__)
        target_folder = '/tmp/unzip_test'
        with Zip_Folder(test_zip) as (zip_file):
            with Unzip_File(zip_file,target_folder,True) as temp_folder:
                assert Files.exists(temp_folder) is True
        assert Files.exists(temp_folder) is False



