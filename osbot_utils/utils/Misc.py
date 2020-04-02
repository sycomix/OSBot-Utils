import hashlib
import json
import random
import string
import textwrap
import re
from time import sleep
from osbot_utils.decorators.Type_Check import function_type_check

@function_type_check
def array_add(array : list, value):
    if value is not None:
        array.append(value)
    return value

@function_type_check
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

def chunks(items:list, split: int):
    if items and split and split > 0:
        for i in range(0, len(items), split):
            yield items[i:i + split]

def class_name(target):
    if target:
        return type(target).__name__
    return None

def get_value(target, key, default=None):
    if target is not None:
        try:
            value = target.get(key)
            if value is not None:
                return value
        except:
            pass
    return default

def get_random_color(max=5):
    if max > 5: max = 5                                                             # add support for more than 5 colors
    colors = ['skyblue', 'darkseagreen', 'palevioletred', 'coral', 'darkgray']
    return colors[random_number(0, max-1)]

def is_number(value):
    try:
        int(value)
        return True
    except:
        pass
    return False

def json_dumps(target, message=None):
    if target:
        return json.dumps(target, indent=4)
    return message

def json_format(target, message=None):
    if target:
        return json.dumps(target, indent=4)
    return message

def json_load(target):
    if target:
        try:
            return json.loads(target)
        except:
            pass
    return None

def none_or_empty(target,field):
    if target:
        value = target.get(field)
        return (value is None) or value == ''
    return True

def object_data(target):
    #fields = [field for field in dir(target) if not callable(getattr(target, field)) and not field.startswith("a__")]
    return target.__dict__ # this one seems to do the trick (if not look at the code sample above)


def random_filename(extension='.tmp', length=10):
    if len(extension) > 0 and  extension[0] != '.' : extension = '.' + extension
    return '{0}{1}'.format(''.join(random.choices(string.ascii_lowercase + string.digits, k=length)) ,  extension)

def random_port(min=20000,max=65000):
    return random_number(min, max)

def random_number(min=1,max=65000):
    return random.randint(min, max)

def random_string_and_numbers(length=6,prefix=''):
    return prefix + ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))

def md5(target):
    if target:
        return hashlib.md5('{0}'.format(target).encode()).hexdigest()
    return None

def trim(target):
    if target:
        return target.strip()
    return target

def to_int(value):
    try:
        return int(value)
    except:
        return 0

def wait(seconds):
    sleep(seconds)

def word_wrap(text,length = 40):
    return '\n'.join(textwrap.wrap(text, length))

def word_wrap_escaped(text,length = 40):
    if text:
        return '\\n'.join(textwrap.wrap(text, length))

def convert_to_number(value):
    if value != '':
        try:
            if value[0] == '£':
                return float(re.sub(r'[^\d.]', '', value))
            else:
                return float(value)
        except:
          return 0
    else:
        return 0

def remove_html_tags(html):
    if html:
        TAG_RE = re.compile(r'<[^>]+>')
        return TAG_RE.sub('', html).replace('&nbsp;', ' ')


def get_field(target, field, default=None):
    if target is not None:
        try:
            value = getattr(target, field)
            if value is not None:
                return value
        except:
            pass
    return default

def get_missing_fields(target,field):
    missing_fields = []
    for field in field:
        if get_field(target, field) is None:
            missing_fields.append(field)
    return missing_fields

def last_letter(text):
    if text and (type(text) is str) and len(text) > 0:
        return text[-1]

def random_text(prefix=None,length=12):
    if prefix is None: prefix = 'text_'
    if last_letter(prefix) != '_':
        prefix += '_'
    return random_string_and_numbers(length=length, prefix=prefix)
