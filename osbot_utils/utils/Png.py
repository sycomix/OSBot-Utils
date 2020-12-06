import base64

from osbot_utils.utils.Dev import Dev

from osbot_utils.utils.Files import temp_file
from osbot_utils.utils.Misc import bytes_to_base64


def save_png_bytes_to_file(bytes, png_file=None, log_status=True):
    png_data = bytes_to_base64(bytes)
    return save_png_base64_to_file(png_data, png_file, log_status)

def save_png_base64_to_file(png_data, png_file=None, log_status=True):
    if png_data is not None:
        if type(png_data) is not str:
            if (log_status):
                Dev.pprint(f'Png data was not a string: {png_data}')
        else:
            if png_file is None:
                png_file = temp_file('.png')
            try:
                with open(png_file, "wb") as fh:
                    fh.write(base64.decodebytes(png_data.encode()))
                if (log_status):
                    Dev.pprint(f'Png data with size {len(png_data)} saved to {png_file}')
                return png_file
            except Exception as error:
                if(log_status):
                    Dev.pprint(f'png save error: {error}')
                    Dev.pprint(png_data)
