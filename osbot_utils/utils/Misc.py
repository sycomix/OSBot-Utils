import base64
import hashlib
import os
import random
import string
import sys
import textwrap
import re
import uuid
import warnings
from datetime   import datetime
from secrets    import token_bytes
from time import sleep

from dotenv     import load_dotenv

def array_add(array : list, value):
    if value is not None:
        array.append(value)
    return value

def array_find(array:list, item):
    if item in array:
        return array.index(item)
    return -1

def array_get(array, position=None, default=None):
    if type(array) is list:
        if type(position) is int and position >=0 :
            if  len(array) > position:
                return array[position]
    return default

def array_pop(array:list, position=None, default=None):
    if array:
        if len(array) >0:
            if type(position) is int:
                if len(array) > position:
                    return array.pop(position)
            else:
                return array.pop()
    return default

def array_pop_and_trim(array, position=None):
    value = array_pop(array,position)
    if type(value) is str:
        return trim(value)
    return value

def bytes_md5(bytes : bytes):
    return hashlib.md5(bytes).hexdigest()

def bytes_sha256(bytes : bytes):
    return hashlib.sha256(bytes).hexdigest()

def base64_to_bytes(bytes_base64):
    if type(bytes_base64) is str:
        bytes_base64 = bytes_base64.encode()
    return base64.decodebytes(bytes_base64)

def base64_to_str(target):
    return bytes_to_str(base64_to_bytes(target))

def bytes_to_base64(bytes):
    return base64.b64encode(bytes).decode()

def bytes_to_str(target, encoding='ascii'):
    return target.decode(encoding=encoding)

def chunks(items:list, split: int):
    if items and split and split > 0:
        for i in range(0, len(items), split):
            yield items[i:i + split]

def class_name(target):
    if target:
        return type(target).__name__

def convert_to_number(value):
    if value:
        try:
            if value[0] in ['£','$','€']:
                return float(re.sub(r'[^\d.]', '', value))
            else:
                return float(value)
        except:
          return 0
    else:
        return 0

def date_now():
    return str(datetime.now())

def env_value(var_name):
    return env_vars().get(var_name, None)

def env_vars():
    """
    reload data from .env file and return dictionary with current environment variables
    """
    load_dotenv()
    vars = os.environ
    data = {}
    for key in vars:
        data[key] = vars[key]
    return data

def env_vars_list():
    return list_set(env_vars())

def flist(target):
    from osbot_utils.fluent.Fluent_List import Fluent_List
    return Fluent_List(target)

def get_field(target, field, default=None):
    if target is not None:
        try:
            value = getattr(target, field)
            if value is not None:
                return value
        except:
            pass
    return default

def get_value(target, key, default=None):
    if target is not None:
        value = target.get(key)
        if value is not None:
            return value
    return default

# todo: check if this should still be here
def get_random_color(max=5):
    if max > 5: max = 5                                                             # add support for more than 5 colors
    colors = ['skyblue', 'darkseagreen', 'palevioletred', 'coral', 'darkgray']
    return colors[random_number(0, max-1)]

def get_missing_fields(target,field):
    missing_fields = []
    for field in field:
        if get_field(target, field) is None:
            missing_fields.append(field)
    return missing_fields

def is_number(value):
    try:
        int(value)
        return True
    except:
        pass
    return False

def ignore_warning_unclosed_ssl():
    warnings.filterwarnings("ignore", category=ResourceWarning, message="unclosed.*<ssl.SSLSocket.*>")

def last_letter(text):
    if text and (type(text) is str) and len(text) > 0:
        return text[-1]

def list_set(target):
    return sorted(list(set(target)))

def list_index_by(values, index_by):
    from osbot_utils.fluent.Fluent_Dict import Fluent_Dict
    results = {}
    for item in values:
        results[item.get(index_by)] = item
    return Fluent_Dict(results)

def list_group_by(values, group_by):
    results = {}
    for item in values:
        value = item.get(group_by)
        if results.get(value) is None: results[value] = []
        results[value].append(item)
    return results

def lower(target : str):
    if target:
        return target.lower()
    return ""

def str_md5(text : str):
    if text:
        return bytes_md5(text.encode())
    return None

def none_or_empty(target,field):
    if target and field:
        value = target.get(field)
        return (value is None) or value == ''
    return True

def str_sha256(text: str):
    if text:
        return bytes_sha256(text.encode())
        #return hashlib.sha256('{0}'.format(text).encode()).hexdigest()
    return None

def random_bytes(length=24):
    return token_bytes(length)

def random_filename(extension='.tmp', length=10):
    from osbot_utils.utils.Files import file_extension_fix
    extension = file_extension_fix(extension)
    return '{0}{1}'.format(''.join(random.choices(string.ascii_lowercase + string.digits, k=length)) ,  extension)

def random_port(min=20000,max=65000):
    return random_number(min, max)

def random_number(min=1,max=65000):
    return random.randint(min, max)

def random_password(length=24, prefix=''):
    password = prefix + ''.join(random.choices(string.ascii_lowercase  +
                                               string.ascii_uppercase +
                                               string.punctuation     +
                                               string.digits          ,
                                               k=length))
    # replace these chars with _  (to make prevent errors in command prompts)
    items = ['"', '\'', '`','\\','}']
    for item in items:
        password = password.replace(item, '_')
    return password

def random_string(length=6,prefix=''):
    return prefix + ''.join(random.choices(string.ascii_uppercase, k=length))

def random_string_and_numbers(length=6,prefix=''):
    return prefix + ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))

def random_text(prefix=None,length=12):
    if prefix is None: prefix = 'text_'
    if last_letter(prefix) != '_':
        prefix += '_'
    return random_string_and_numbers(length=length, prefix=prefix)

def random_uuid():
    return str(uuid.uuid4())

def remove(target_string, string_to_remove):
    return replace(target_string, string_to_remove, '')

def remove_multiple_spaces(target):
    return re.sub(' +', ' ', target)

def replace(target_string, string_to_find, string_to_replace):
    return target_string.replace(string_to_find, string_to_replace)

def remove_html_tags(html):
    if html:
        TAG_RE = re.compile(r'<[^>]+>')
        return TAG_RE.sub('', html).replace('&nbsp;', ' ')

def split_lines(text):
    return text.replace('\r\n','\n').split('\n')

def split_spaces(target):
    return remove_multiple_spaces(target).split(' ')

def sorted_set(target : object):
    if target:
        return sorted(set(target))
    return []

def str_to_base64(target):
    return bytes_to_base64(str_to_bytes(target))

def str_to_bytes(target):
    return target.encode()

def str_to_date(str_date, format='%Y-%m-%d %H:%M:%S.%f'):
    return datetime.strptime(str_date,format)

def to_int(value, default=0):
    try:
        return int(value)
    except:
        return default

def trim(target):
    if type(target) is str:
        return target.strip()
    return ""

def under_debugger():
    return 'pydevd' in sys.modules

def upper(target : str):
    if target:
        return target.upper()
    return ""

def wait(seconds):
    sleep(seconds)

def word_wrap(text,length = 40):
    return '\n'.join(textwrap.wrap(text, length))

def word_wrap_escaped(text,length = 40):
    if text:
        return '\\n'.join(textwrap.wrap(text, length))

bytes_to_string  = bytes_to_str
convert_to_float = convert_to_number
new_guid         = random_uuid
str_lines        = split_lines