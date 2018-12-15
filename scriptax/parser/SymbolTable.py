from scriptax.parser.symbols.SymbolTable import SymbolTable as GenericTable
from scriptax.parser.symbols.SymbolScope import SymbolScope, SCOPE_MODULE, SCOPE_GLOBAL, SCOPE_BLOCK
from scriptax.parser.symbols.Symbol import Symbol, DATA_DICT, DATA_LIST, DATA_INSTANCE, DATA_PYTHONIC, DATA_THREAD, \
    SYMBOL_VAR


class SymbolTable(GenericTable):
    def __init__(self, name=None, type=SCOPE_MODULE):
        super().__init__(name, type)
        self.up_words = ['parent', 'self', 'this', 'me']

    # Returns whether or not the name has an 'up' keyword anywhere in it
    def name_has_up(self, name: list):
        return any(keyword in self.up_words for keyword in name)

    # Verifies a name to be valid
    # Ensures that only the first name element is an 'up' keyword
    def is_name_valid(self, name: list):
        if self.name_has_up(name[1:]):
            return False
        return True

    # Splits a string name into a list name
    # Also verifies the name has broadly correct syntax.
    def make_and_verify_name(self, name: str):
        comps = name.strip().split('.')
        if not self.is_name_valid(comps):
            raise Exception("Invalid symbol access `" + name + "` Scriptax.SymbolTable@make_and_verify_name")
        return comps

    # Returns the proper static parent scope based on up traversals
    # Because name is a mutable list, it will return without any up traversal keywords left in it
    def traverse_up(self, name: list):
        scope = self.scope()
        if self.name_has_up([name[0]]):
            while scope.type != SCOPE_MODULE:
                scope = scope.scope_parent
                name.pop(0)
                if not scope:
                    raise Exception("Invalid symbol access. Too many up traversals. Scriptax.SymbolTable@traverse_up")
        return scope

    # Traverses through a scope and its appropriate static parents to try and find a symbol
    def search_scope_for_symbol(self, scope: SymbolScope, name: str, type=SYMBOL_VAR):

        while scope:
            if scope.has_symbol(name, symbol_type=type):
                return scope.get_symbol(name, symbol_type=type)

            if scope.type == SCOPE_MODULE and scope.scope_parent and scope.scope_parent.type == SCOPE_MODULE:
                scope = scope.scope_parent
            elif scope.type == SCOPE_BLOCK and scope.scope_parent and scope.scope_parent.type == SCOPE_BLOCK:
                scope = scope.scope_parent
            else:
                raise Exception(
                    "Cannot find symbol `" + name + "` inside of scope `" + scope.name + "`. Scriptax.SymbolTable@search_scope_for_symbol")

    # Traverses through symbol values to try and find a value
    def search_symbol_for_value(self, symbol: Symbol, name: list, type=SYMBOL_VAR):
        while len(name) > 0:
            if symbol.data_type == DATA_INSTANCE:
                symbol = self.search_scope_for_symbol(symbol.value, name[0], type)

            elif symbol.data_type == DATA_LIST:
                try:
                    symbol = symbol.value[int(name[0])]
                except:
                    raise Exception("Invalid list access `" + name[0] + "` for symbol value `" + str(
                        symbol.value) + "`. Scriptax.SymbolTable@search_symbol_for_value")
                if not isinstance(symbol, Symbol):
                    symbol = Symbol(name=name[0], value=symbol)

            elif symbol.data_type == DATA_DICT:
                try:
                    symbol = symbol.value[str(name[0])]
                except:
                    raise Exception("Invalid dict access `" + name[0] + "` for symbol value `" + str(
                        symbol.value) + "`. Scriptax.SymbolTable@search_symbol_for_value")
                if not isinstance(symbol, Symbol):
                    symbol = Symbol(name=name[0], value=symbol)

            elif symbol.data_type == DATA_PYTHONIC:
                symbol = Symbol(name=name[0], value=None)

            elif symbol.data_type == DATA_THREAD:
                symbol = Symbol(name=name[0], value=None)

            else:
                raise Exception("Unsupported symbol access `" + name[0] + "` for symbol value `" + str(
                    symbol.value) + "`. Scriptax.SymbolTable@search_symbol_for_value")

            name.pop(0)

        return symbol.value

    def set_symbol(self, name: str, value, type=SYMBOL_VAR):
        name: list = self.make_and_verify_name(name)
        scope: SymbolScope = self.traverse_up(name)
        try:
            symbol: Symbol = self.search_scope_for_symbol(scope, name[0], type)
        except:
            if len(name) > 1:
                raise Exception(
                    "Variable access contains too many components for uninitialized subcomponent `" + "".join(
                        name) + "`. Scriptax.SymbolTable@set_symbol")
            scope.insert_symbol(Symbol(name=name[0], value=value))
            return

        try:
            name.pop(0)
            if len(name) > 0:
                index = name[-1]
                symbol = Symbol(name="".join(name), value=self.search_symbol_for_value(symbol, name[:-1], type))
                if symbol.data_type == DATA_INSTANCE:
                    symbol = symbol.value.get_symbol(index)
                    symbol.value = value
                elif symbol.data_type == DATA_DICT:
                    symbol.value[str(index)] = value
                elif symbol.data_type == DATA_DICT:
                    symbol.value[int(index)] = value
                else:
                    raise Exception("Unsupported symbol access `" + index + "` for symbol value `" + str(
                        symbol.value) + "`. Scriptax.SymbolTable@set_symbol")
            else:
                symbol.value = value
        except:
            raise Exception("Alterring existing symbol failed. Scriptax.SymbolTable@set_symbol")

    # Returns whether or not the given symbol exists
    def has_symbol(self, name, type=SYMBOL_VAR) -> bool:
        try:
            self.get_symbol_value(name, type)
        except:
            return False
        return True

    # Returns a symbol object for a given name
    # Returns symbol or the traversed symbol value
    def get_symbol(self, name: str, type=SYMBOL_VAR, as_value=True):
        name: list = self.make_and_verify_name(name)
        scope: SymbolScope = self.traverse_up(name)
        symbol: Symbol = self.search_scope_for_symbol(scope, name[0], type)
        name.pop(0)
        if as_value:
            return self.search_symbol_for_value(symbol, name, type)
        return symbol

    def remove_symbol(self, name: str, type=SYMBOL_VAR):
        pass

    def execute(self, name, parameters):
        pass

    # No parameters on this one as it is handled via the constructor
    def new(self, name):
        # TODO add a symbol which is of type scope
        pass

    def copy(self, name):
        # TODO copies a scope via the passed in name
        pass
