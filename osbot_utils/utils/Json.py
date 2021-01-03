import json
import gzip
import logging
import os

log = logging.getLogger()   # todo: start using this API for capturing error messages from methods bellow

from osbot_utils.utils.Files import file_exists, temp_file, file_create_gz, file_create, load_file_gz, file_contents


class Json:

    @staticmethod
    def dumps(python_object, indent=4, pretty=True):
        if python_object:
            try:
                if pretty:
                    return json.dumps(python_object, indent=indent)
                return json.dumps(python_object)
            except:
                log.exception('Error in load_json')

    @staticmethod
    def get_logger():
        return log

    @staticmethod
    def load_file(path):
        """
        Loads json data from file
        Note: will not throw errors and will return {} as default
        errors are logged to Json.log
        """
        json_data = file_contents(path)
        return json_loads(json_data)

    @staticmethod
    def load_file_and_delete(path):
        data = json_load_file(path)
        if data:
            os.remove(path)
        return data

    @staticmethod
    def load_file_gz(path):
        if os.path.exists(path) is False:
            return None
        data = load_file_gz(path)
        return json_loads(data)

    @staticmethod
    def load_file_gz_and_delete(path):
        data = Json.load_json_gz(path)
        if data:
            os.remove(path)
        return data

    @staticmethod
    def loads(json_data):
        """
        Loads json data from string
        Note: will not throw errors and will return {} as default
        errors are logged to Json.log
        """
        if json_data:
            try:
                return json.loads(json_data)
            except:
                log.exception('Error in load_json')
        return {}

    @staticmethod
    def round_trip(data):
        return json.loads(json.dumps(data))

    @staticmethod
    def save_file(python_object, path=None, pretty=False):
        json_data = json_dumps(python_object=python_object, indent=2, pretty=pretty)
        return file_create(path=path, contents=json_data)

    @staticmethod
    def save_file_pretty(python_object, path=None):
        return json_save_file(python_object=python_object, path=path, pretty=True)

    @staticmethod
    def save_file_gz(python_object, path=None, pretty=False):
        json_data = json_dumps(python_object,indent=2, pretty=pretty)
        return file_create_gz(path=path, contents=json_data)

        # with gzip.open(path, 'w') as fp:
        #     fp.write(json_dump.encode())
        # return path

        # json_dump = json.dumps(data)
        # with gzip.open(path, 'w') as fp:        # todo refactor to use Files methods
        #     fp.write(json_dump.encode())
        # return path

    @staticmethod
    def save_file_pretty_gz(python_object, path=None):
        return json_save_file_gz(python_object=python_object, path=path, pretty=True)


    @staticmethod
    def json_save_tmp_file(python_object, pretty=True):
        return Json.save_file(python_object=python_object, pretty=pretty, path=None)

    @staticmethod
    def save_json_pretty(path, data):
        return Json.save_file(path, data, pretty=True)

json_dumps                  = Json.dumps
json_format                 = Json.dumps
json_load_file              = Json.load_file
json_load_file_gz           = Json.load_file_gz
json_load_file_and_delete   = Json.load_file_and_delete
json_from_string            = Json.loads
json_loads                  = Json.loads
json_parse                  = Json.loads
json_round_trip             = Json.round_trip
json_save                   = Json.save_file
json_save_file              = Json.save_file
json_save_file_pretty       = Json.save_file_pretty
json_save_file_gz           = Json.save_file_gz
json_save_file_pretty_gz    = Json.save_file_pretty_gz
json_save_tmp_file          = Json.json_save_tmp_file