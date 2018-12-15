from antlr4.ParserRuleContext import ParserRuleContext
from scriptax.utilities.Hex import instance_to_hexid
import threading

# Data Types
DATA_NUMBER = 'number'
DATA_BOOLEAN = 'boolean'
DATA_HEX = 'hex'
DATA_NONE = 'none'
DATA_STRING = 'string'
DATA_DICT = 'dict'
DATA_LIST = 'list'
DATA_METHOD = 'method'
DATA_THREAD = 'thread'  # Holds python threading object
DATA_PYTHONIC = 'pythonic'  # Some other arbitrary python class/object
DATA_INSTANCE = 'instance'  # Holds an instance of a class/script type

# Symbol Types
SYMBOL_VAR = 'var'
SYMBOL_MODULE = 'module'


# Type inference
def value_to_type(value):
    from scriptax.parser.symbols.SymbolScope import SymbolScope
    if type(value) is bool:
        return DATA_BOOLEAN
    if isinstance(value, (float, int)):
        return DATA_NUMBER
    if isinstance(value, str) and value[:2].lower() == '0x':
        return DATA_HEX
    if isinstance(value, str):
        return DATA_STRING
    if isinstance(value, dict):
        return DATA_DICT
    if isinstance(value, list):
        return DATA_LIST
    if value is None:
        return DATA_NONE
    if isinstance(value, threading.Thread):
        return DATA_THREAD
    if isinstance(value, ParserRuleContext):
        return DATA_METHOD
    if isinstance(value, SymbolScope):
        return DATA_INSTANCE
    return DATA_PYTHONIC


class Symbol:
    def __init__(self, name, value=None, symbol_type=SYMBOL_VAR, data_type=None, attributes=None):
        self.name = name

        if not data_type:
            self.data_type = value_to_type(value)
        else:
            self.data_type = data_type

        self.symbol_type = symbol_type

        self.value = value

        self.attributes = attributes
        if not self.attributes:
            self.attributes = {}

    def set_value(self, data_type=None, value=None):
        if not data_type:
            self.data_type = value_to_type(value)
        else:
            self.data_type = data_type
        self.value = value

    def get_symbol_debug(self):
        from scriptax.parser.symbols.SymbolScope import SymbolScope

        value = str(self.value)

        if isinstance(self.value, SymbolScope):
            value = {"pointer": {"reference": value, "pointing-to-scope": instance_to_hexid(self.value)}}

        return {
            'name': self.name,
            'symbol-type': str(self.symbol_type),
            'data-type': str(self.data_type),
            'value': value,
            'attributes': self.attributes
        }

    def print_symbol_debug(self):
        print(self.get_symbol_debug())
