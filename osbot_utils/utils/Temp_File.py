from osbot_utils.utils.Files import Files
from osbot_utils.utils.Misc import Misc


class Temp_File:
    def __init__(self, contents='...', extension='tmp'):
        self.tmp_file   = Misc.random_filename(extension)
        self.tmp_folder = Files.temp_folder()
        self.file_path  = Files.path_combine(self.tmp_folder, self.tmp_file)
        self.contents   = contents

    def __enter__(self):
        Files.write(self.file_path, self.contents)
        return self

    def __exit__(self, type, value, traceback):
        Files.delete(self.file_path)