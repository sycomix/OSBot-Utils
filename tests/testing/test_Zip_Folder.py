import json
from unittest import TestCase

from osbot_utils.testing.Zip_Folder import Zip_Folder
from osbot_utils.utils.Files import Files, parent_folder


class test_Zip_Folder(TestCase):

    def test__using_with__no_params(self):
        with Zip_Folder() as (zip_file):
            assert zip_file is None

    def test__using_with_params(self):
        target_folder = parent_folder(__file__)
        with Zip_Folder(target_folder) as (zip_file):
            assert Files.exists(zip_file) is True
        assert Files.exists(zip_file) is False



