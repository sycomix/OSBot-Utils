from unittest import TestCase

import pytest

from osbot_utils.utils.Csv import load_csv_from_file, load_csv_from_str, load_csv_from_url
from osbot_utils.utils.Files import file_create, file_delete

csv_string = """a,b,c\n1,2,3\nx,y,z"""
class Test_Csv(TestCase):

    def setUp(self) -> None:
        self.file_path = file_create(contents=csv_string)

    def tearDown(self) -> None:
        file_delete(self.file_path)

    def test_load_csv_from_file(self):
        csv_content = load_csv_from_file(self.file_path)

        assert len(csv_content) == 2
        assert csv_content.__getitem__(0).get('a') == '1'
        assert csv_content.__getitem__(1).get('b') == 'y'

    def test_load_csv_from_string(self):
        csv_content = load_csv_from_str(csv_string)

        assert len(csv_content) == 2
        assert csv_content.__getitem__(0).get('a') == '1'
        assert csv_content.__getitem__(1).get('b') == 'y'

    @pytest.mark.skip("todo: figure out why this tests started failing intermittently (on Oct 2023)")
    def test_load_csv_from_url(self):
        sample_url  = 'https://filesamples.com/samples/document/csv/sample1.csv'
        headers     = {"User-Agent"     : "Mozilla/5.0"}
        csv_content = load_csv_from_url(sample_url, headers)

        self.assertIsNotNone(csv_content)


