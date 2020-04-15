from unittest import TestCase

from osbot_utils.utils.Json import json_save_tmp_file, json_load


class test_Json(TestCase):

    def test_json_load__json_save_tmp_file(self):
        data = {'answer': 42}
        json_file = json_save_tmp_file(data)
        assert json_load(json_file) == data
