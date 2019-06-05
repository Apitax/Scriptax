from antlr4.ParserRuleContext import ParserRuleContext
from scriptax.utilities.Hex import instance_to_hexid
from typing import Any
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


def value_to_type(value):
    """
    Used to dynamically determine the type of a value

    Parameters
    ----------
    value : Any
        The value we are trying to determine the type of

    Returns
    -------
    str
        The text name of the value's type
    """
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
    """
    Represents a symbol

    ...

    Attributes
    ----------
    name : str
        The name of this symbol. Typically the name of a variable or the name of a method
    value : any, optional
        The value associated to this symbol
    symbol_type : str, optional
        Is this symbol a variable or a module
    data_type : str, optional
        Do we already know the data type of the value, or do we wish to enforce one
    attributes : dict, optional
        Metadata which we need to associate to this symbol

    Methods
    -------
    set_value(data_type=None, value=None)
    get_symbol_debug()
    print_symbol_debug()
    """

    def __init__(self, name: str, value: Any = None, symbol_type: str = SYMBOL_VAR, data_type: str = None,
                 attributes: dict = None):
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

    def set_value(self, data_type: str = None, value: Any = None):
        """
        Sets the value of a symbol
        """
        if not data_type:
            self.data_type = value_to_type(value)
        else:
            self.data_type = data_type
        self.value = value

    def get_symbol_debug(self) -> dict:
        """
        Retrieve information about the symbol
        """
        from scriptax.parser.symbols.SymbolScope import SymbolScope

        value = self.value
        if not isinstance(value, (str, float, int, bool, dict, list)):
            value = str(value)

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
        """
        Print information about the symbol
        """
        print(self.get_symbol_debug())
