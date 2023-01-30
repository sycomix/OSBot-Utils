from html import escape, unescape

from osbot_utils.utils.Files import safe_file_name


def html_escape(value):
    return escape(value)

def html_unescape(value):
    return unescape(value)

def str_join(delimiter, values):
    return delimiter.join(values)

def str_safe(value):
    return safe_file_name(value)

html_encode = html_escape
html_decode = html_unescape