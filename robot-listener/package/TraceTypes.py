from enum import Enum
from collections import namedtuple

# Available colors
class Color(Enum):
    red    = "\033[91m"
    green  = "\033[92m"
    cyan   = "\033[36m"
    blue   = "\033[34m"

# Availablre text formats
class TextFormat(Enum):
    clear  = "\033[0m"
    bold   = "\033[1m"
    italic = "\033[3m"

# modify these labels to match your style/meet terminal constraints
class Label(Enum):
    success = '✅'
    fail = '❌'
    busy = '⌛'
    log = '🤖'
    sleep = '💤'
    call = '↪'

# Trace represents an object that is later converted to a string taking in
# consideration its properties
class Trace(namedtuple('Trace', ['label', 'color', 'text', 'text_format'])):
    def __new__(cls, label='', color='', text='', text_format=''):
        return super().__new__(cls, label, color, text, text_format)