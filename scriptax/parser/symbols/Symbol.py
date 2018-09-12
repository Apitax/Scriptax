from antlr4.ParserRuleContext import ParserRuleContext
import threading

SYMBOL_SCRIPT = 'script'
SYMBOL_METHOD = 'method'
SYMBOL_VARIABLE = 'variable'

DATA_NUMBER = 'number'
DATA_BOOLEAN = 'boolean'
DATA_HEX = 'hex'
DATA_NONE = 'none'
DATA_STRING = 'string'
DATA_DICT = 'dict'
DATA_LIST = 'list'
DATA_THREAD = 'thread'
DATA_PYTHONIC = 'pythonic'  # Some other arbitrary python class/object
DATA_CONTEXT = 'context'


# Type inference helper method
def valueToType(value):
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
        return DATA_CONTEXT
    return DATA_PYTHONIC


class Symbol:
    def __init__(self, name=None, symbolType=None, dataType=None, value=None):
        self.name = name
        self.symbolType = symbolType
        if not dataType:
            self.dataType = valueToType(value)
        else:
            self.dataType = dataType
        self.value = value
