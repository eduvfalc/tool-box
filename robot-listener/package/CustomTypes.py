from enum import Enum
from collections import namedtuple

# ANSI color codes
class Color(Enum):
    red    = "\033[91m"
    green  = "\033[92m"
    reset  = "\033[0m"
    bold   = "\033[1m"
    italic = "\033[3m"
    clear  = "\033[K"
    cyan   = "\033[36m"
    blue   = "\033[34m"

# Labels
class Label(Enum):
    success = '✅ '
    fail = '❌ '
    busy = '⌛ '
    call = f'{Color.bold.value}↪{Color.reset.value} '
    log = '🤖 '

# Define the base namedtuple class
class Trace(namedtuple('Trace', ['label', 'color', 'text'])):
    __slots__ = ()  # To prevent unnecessary memory usage for instance dictionaries

    # Override __new__ to set default values
    def __new__(cls, label='', color='', text=''):
        return super().__new__(cls, label, color, text)