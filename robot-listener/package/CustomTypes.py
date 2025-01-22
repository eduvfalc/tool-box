from enum import Enum
from collections import namedtuple

class Color(Enum):
    red    = "\033[91m"
    green  = "\033[92m"
    reset  = "\033[0m"
    bold   = "\033[1m"
    italic = "\033[3m"
    cyan   = "\033[36m"
    blue   = "\033[34m"

class Label(Enum):
    success = '✅'
    fail = '❌'
    busy = '⌛'
    log = '🤖'
    call = f'{Color.bold.value}↪{Color.reset.value} '

class Trace(namedtuple('Trace', ['label', 'color', 'text'])):
    def __new__(cls, label='', color='', text=''):
        return super().__new__(cls, label, color, text)