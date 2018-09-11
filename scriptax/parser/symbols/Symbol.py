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
DATA_PYTHONIC = 'pythonic'
DATA_CONTEXT = 'context'


class Symbol:
    def __init__(self, name=None, symbolType=None, dataType=None, value=None):
        self.name = name
        self.symbolType = symbolType
        self.dataType = dataType
        self.value = value
