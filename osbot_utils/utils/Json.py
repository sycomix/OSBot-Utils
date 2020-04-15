import json
import gzip
import logging
import os

log = logging.getLogger()   # todo: start using this API for capturing error messages from methods bellow

from osbot_utils.utils.Files import file_exists, temp_file


def json_load         (path                   ): return Json.load_json(path)
def json_save         (path, data, pretty=True): return Json.save_json(path, data, pretty)
def json_save_tmp_file(      data, pretty=True): return Json.save_json(None, data, pretty)

class Json:

    @staticmethod
    def load_json(path):
        """Note: will not throw errors and will return {} as default"""
        try:
            if file_exists(path):
                with open(path, "rt") as fp:
                    data = fp.read()
                    return json.loads(data)
        except:
            log.exception('Error in load_json')
        return {}

    @staticmethod
    def load_json_and_delete(path):
        data = Json.load_json(path)
        if data:
            os.remove(path)
        return data

    @staticmethod
    def load_json_gz(path):
        if os.path.exists(path) is False:
            return None
        with gzip.open(path, "rt") as fp:
            data = fp.read()
            return json.loads(data)

    @staticmethod
    def load_json_gz_and_delete(path):
        data = Json.load_json_gz(path)
        if data:
            os.remove(path)
        return data

    @staticmethod
    def save_json_gz(path, data):
        json_dump = json.dumps(data)
        with gzip.open(path, 'w') as fp:
            fp.write(json_dump.encode())
        return path

    @staticmethod
    def save_json_gz_pretty(path, data):
        json_dump = json.dumps(data,indent=2)
        with gzip.open(path, 'w') as fp:
            fp.write(json_dump.encode())
        return path

    @staticmethod
    def save_json(path, data, pretty=True):
        if path is None:
            path = temp_file()
        if pretty:
            json_dump = json.dumps(data, indent=2)
        else:
            json_dump = json.dumps(data)
        with open(path, 'w') as fp:
            fp.write(json_dump)
        return path

    @staticmethod
    def save_json_pretty(path, data):
        return Json.save_json(path, data, pretty=True)