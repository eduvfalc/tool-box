from enum import Enum
from collections import namedtuple

class Color(Enum):
    red    = "\033[91m"
    green  = "\033[92m"
    cyan   = "\033[36m"
    blue   = "\033[34m"

class TextFormat(Enum):
    clear  = "\033[0m"
    bold   = "\033[1m"
    italic = "\033[3m"

class Label(Enum):
    success = '✅'
    fail = '❌'
    busy = '⌛'
    log = '🤖'
    call = '↪'

class Trace(namedtuple('Trace', ['label', 'color', 'text', 'text_format'])):
    def __new__(cls, label='', color='', text='', text_format=''):
        return super().__new__(cls, label, color, text, text_format)