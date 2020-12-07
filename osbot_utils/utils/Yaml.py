import yaml

from osbot_utils.utils.Files import temp_file


class Yaml:
    @staticmethod
    def yaml_load(path_file):
        with open(path_file) as file:
            return yaml.safe_load(file)

    @staticmethod
    def yaml_parse(yaml_code):
        return yaml.safe_load(yaml_code)

    @staticmethod
    def yaml_save(yaml_code, path_file=None):       #todo: refactor other 'save' methods to have the content as the first param (to allow for creation of temp files when path_file path is not provided)
        if path_file is None:
            path_file = temp_file(extension=".yaml")
        with open(path_file, 'w') as file:
            yaml.dump(yaml_code, file)
        return path_file

# also add these methods to the top level to allow direct import and usage (without the Yaml.*)
yaml_load  = Yaml.yaml_load
yaml_parse = Yaml.yaml_parse
yaml_save  = Yaml.yaml_save