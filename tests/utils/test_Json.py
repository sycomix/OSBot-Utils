from pprint import pprint
from unittest import TestCase

from osbot_utils.utils.Files import file_exists, load_file_gz, file_lines_gz
from osbot_utils.utils.Json import json_save_tmp_file, json_parse, json_loads, json_dumps, json_format, \
    json_load_file, json_load_file_and_delete, json_save_file_gz, json_save_file_pretty_gz, json_load_file_gz, \
    json_round_trip, Json


class test_Json(TestCase):

    def test_json_parse__json_format__json_dumps__json_loads(self):
        # data = {'answer': 42 }
        # assert json_dumps (data) == '{\n    "answer": 42\n}'
        # assert json_format(data) == '{\n    "answer": 42\n}'
        # assert json_parse (json_dumps(data)) == data
        # assert json_loads (json_dumps(data)) == data
        #
        # assert json_dumps (None) is None
        # assert json_format(None) is None
        # assert json_parse (None) == {}
        # assert json_loads (None) == {}


        import logging
        print()

        from io import StringIO
        stream = StringIO()
        log = Json.get_logger()

        handler = logging.StreamHandler(stream)
        log.addHandler(handler)
        print(stream.getvalue())
        #print(json_loads("{ bad : json }") )
        print(stream.getvalue())

    def test_json_load_file__json_save_tmp_file(self):
        data = {'answer': 42 }
        json_file = json_save_tmp_file(data)
        assert file_exists(json_file)
        assert json_load_file(json_file) == data
        assert file_exists(json_file)

    def test_json_load_file_and_delete(self):
        data = {'answer': 42 }
        json_file = json_save_tmp_file(data)
        assert file_exists(json_file) is True
        assert json_load_file_and_delete(json_file) == data
        assert file_exists(json_file) is False

    def test_json_load_file_gz__json_save_file_pretty_gz(self):
        data = {'answer': 42}
        gz_file = json_save_file_pretty_gz(data)
        json_load_file_gz(gz_file) == data


    def test_json_round_trip(self):
        data = {'answer': 42}
        assert json_round_trip(data) == data
    # def test_json_load__json_save_tmp_file(self):
    #     data = {'answer': 42}
    #     json_file = json_save_tmp_file(data)
    #     assert json_load(data=json_file) == data
