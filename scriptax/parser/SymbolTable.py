from typing import List
from scriptax.models.Parameter import Parameter
from scriptax.parser.symbols.ARISymbolTable import ARISymbolTable as GenericTable
from scriptax.parser.symbols.ARISymbolTable import create_table as create_generic_table
from scriptax.parser.symbols.SymbolScope import SymbolScope, SCOPE_MODULE, SCOPE_BLOCK
from scriptax.parser.symbols.Symbol import Symbol, DATA_DICT, DATA_LIST, DATA_INSTANCE, DATA_PYTHONIC, DATA_THREAD, \
    DATA_METHOD, SYMBOL_VAR, SYMBOL_MODULE


class SymbolTable(GenericTable):
    """
    A specialized Symbol Table for Scriptax
    """
    def __init__(self, name=None, type=SCOPE_MODULE):
        super().__init__(name, type)
        self.up_words = ['parent', 'self', 'this', 'me']

    def name_has_up(self, name: list):
        """
        Returns whether or not the name has an 'up' keyword anywhere in it
        """
        return any(keyword in self.up_words for keyword in name)


    def is_name_valid(self, name: list):
        """
        Verifies a name to be valid
        Ensures that only the first name element is an 'up' keyword
        """
        if self.name_has_up(name[1:]):
            return False
        return True


    def make_and_verify_name(self, name: str):
        """
        Splits a string name into a list name
        Also verifies the name has broadly correct syntax.
        """
        comps = name.strip().split('.')
        if not self.is_name_valid(comps):
            raise Exception("Invalid symbol access `" + name + "` Scriptax.SymbolTable@make_and_verify_name")
        return comps


    def traverse_up(self, name: list):
        """
        Returns the proper static parent scope based on up traversals
        Because name is a mutable list, it will return without any up traversal keywords left in it
        """
        scope = self.scope()
        if self.name_has_up([name[0]]):
            while scope.type != SCOPE_MODULE:
                scope = scope.scope_parent
                name.pop(0)
                if not scope:
                    raise Exception("Invalid symbol access. Too many up traversals. Scriptax.SymbolTable@traverse_up")
        return scope


    def _get_parent_module(self):
        """
        Returns the parent module within this static scope
        """
        name = [self.up_words[0]]
        return self.traverse_up(name)


    def search_scope_for_symbol(self, scope: SymbolScope, name: str, type=SYMBOL_VAR) -> Symbol:
        """
        Traverses through a scope and its appropriate static parents to try and find a symbol
        """

        while scope:
            # If symbol is in current scope, then return
            if scope.has_symbol(name, symbol_type=type):
                return scope.get_symbol(name, symbol_type=type)

            # Goes up the inheritance scope tree. Classes
            if scope.type == SCOPE_MODULE and scope.scope_parent and scope.scope_parent.type == SCOPE_MODULE:
                scope = scope.scope_parent

            # Goes up the block scope tree. IF's, LOOP's, Methods
            elif scope.type == SCOPE_BLOCK and scope.scope_parent and scope.scope_parent.type == SCOPE_BLOCK:
                scope = scope.scope_parent

            # If type is GLOBAL or invalid, throw exception
            else:
                raise Exception(
                    "Cannot find symbol `" + name + "` inside of scope `" + scope.name + "`. Scriptax.SymbolTable@search_scope_for_symbol")


    def search_symbol_for_value(self, symbol: Symbol, name: list, type=SYMBOL_VAR):
        """
        Traverses through symbol values to try and find a value
        """

        # One at a time, loops through each component of the name
        while len(name) > 0:
            # If the current symbol is of type INSTANCE (Storing another scope)
            if symbol.data_type == DATA_INSTANCE:
                symbol = self.search_scope_for_symbol(symbol.value, name[0], type)

            # If current scope is of type LIST
            elif symbol.data_type == DATA_LIST:
                try:
                    symbol = symbol.value[int(name[0])]
                except:
                    raise Exception("Invalid list access `" + name[0] + "` for symbol value `" + str(
                        symbol.value) + "`. Scriptax.SymbolTable@search_symbol_for_value")
                if not isinstance(symbol, Symbol):
                    symbol = Symbol(name=name[0], value=symbol)

            # If current scope is of type DICT
            elif symbol.data_type == DATA_DICT:
                try:
                    symbol = symbol.value[str(name[0])]
                except:
                    raise Exception("Invalid dict access `" + name[0] + "` for symbol value `" + str(
                        symbol.value) + "`. Scriptax.SymbolTable@search_symbol_for_value")
                if not isinstance(symbol, Symbol):
                    symbol = Symbol(name=name[0], value=symbol)

            # If current scope is of type PYTHONIC
            elif symbol.data_type == DATA_PYTHONIC:
                symbol = Symbol(name=name[0], value=None)

            # If current scope is of type THREAD
            elif symbol.data_type == DATA_THREAD:
                symbol = Symbol(name=name[0], value=None)

            else:
                raise Exception("Unsupported symbol access `" + name[0] + "` for symbol value `" + str(
                    symbol.value) + "`. Scriptax.SymbolTable@search_symbol_for_value")

            name.pop(0)

        return symbol.value

    def set_symbol(self, name: str, value, type=SYMBOL_VAR):
        """
        Set's the value of an existing symbol, creates the symbol if it does not exist yet, handles LIST and DICT as well
        """

        name: list = self.make_and_verify_name(name)
        scope: SymbolScope = self.traverse_up(name)

        # See if a symbol already exists, if not, it excepts and will insert a new symbol
        try:
            symbol: Symbol = self.search_scope_for_symbol(scope, name[0], type)
        except:
            # If we are inserting a new symbol, then the symbol name must only have a single component
            if len(name) > 1:
                raise Exception(
                    "Variable access contains too many components for uninitialized subcomponent `" + "".join(
                        name) + "`. Scriptax.SymbolTable@set_symbol")
            scope.insert_symbol(Symbol(name=name[0], value=value))
            return

        # If a symbol already exists, this section will modify its value
        try:
            # Pops the name we used to find the starting symbol from the first try/except above
            name.pop(0)
            # If the name still has more components, then we haven't yet found the right value to modify
            if len(name) > 0:
                # Index holds the last component in the name
                index = name[-1]
                # Finds the symbol corresponding to the name excluding the last name component
                symbol = Symbol(name="".join(name), value=self.search_symbol_for_value(symbol, name[:-1], type))
                # If the symbol is an INSTANCE (Another scope), then find the symbol in that scope and modify its value
                # This will not insert a brand new symbol into the scope, thus all symbols MUST be pre-defined in the
                #   scope
                if symbol.data_type == DATA_INSTANCE:
                    symbol = symbol.value.get_symbol(index)
                    symbol.value = value
                # If the symbol is a DICT, add it via dictionary indexing
                elif symbol.data_type == DATA_DICT:
                    symbol.value[str(index)] = value
                # If the symbol is a LIST, add it via numeric index
                elif symbol.data_type == DATA_DICT:
                    symbol.value[int(index)] = value
                # If the symbol is any other type, then we should not be able to apply another name component to it,
                #   thus it is an error
                else:
                    raise Exception("Unsupported symbol access `" + index + "` for symbol value `" + str(
                        symbol.value) + "`. Scriptax.SymbolTable@set_symbol")
            else:
                # If the name has no more components, we have already found the symbol we want to modify
                symbol.value = value
        except:
            raise Exception("Altering existing symbol failed. Scriptax.SymbolTable@set_symbol")


    def has_symbol(self, name: str, type=SYMBOL_VAR) -> bool:
        """
        Returns whether or not the given symbol exists
        """

        try:
            self.get_symbol(name, type)
        except:
            return False
        return True


    def get_symbol(self, name: str, type=SYMBOL_VAR, as_value=True):
        """
        Returns a symbol object for a given name
        Returns symbol or the traversed symbol value
        """

        name: list = self.make_and_verify_name(name)
        scope: SymbolScope = self.traverse_up(name)
        # Gets the symbol from the first level name component
        symbol: Symbol = self.search_scope_for_symbol(scope, name[0], type)
        name.pop(0)
        # Gets value out of the symbol if we desire this
        if as_value:
            return self.search_symbol_for_value(symbol, name, type)
        return symbol

    def remove_symbol(self, name: str, type=SYMBOL_VAR):
        """
        Remove a symbol
        """

        if not self.has_symbol(name, type):
            raise Exception(
                "Cannot remove symbol with name `" + name + "` as it does not exist within this scope. Scriptax.SymbolTable@remove_symbol")

        name: list = self.make_and_verify_name(name)
        scope: SymbolScope = self.traverse_up(name)

        # See if a symbol already exists, if not, it excepts and will insert a new symbol
        try:
            symbol: Symbol = self.search_scope_for_symbol(scope, name[0], type)
        except:
            raise Exception(
                "Cannot remove symbol with name `" + "".join(
                    name) + "` as it does not exist within this scope. Scriptax.SymbolTable@remove_symbol")

        # If a symbol exists, this section will remove it
        try:
            # Pops the name we used to find the starting symbol from the first try/except above
            name.pop(0)
            # If the name still has more components, then we haven't yet found the right symbol to remove
            if len(name) > 0:
                # Index holds the last component in the name
                index = name[-1]
                # Finds the symbol corresponding to the name excluding the last name component
                symbol = Symbol(name="".join(name), value=self.search_symbol_for_value(symbol, name[:-1], type))
                # If the symbol is an INSTANCE (Another scope), then find the symbol in that scope and remove it
                if symbol.data_type == DATA_INSTANCE:
                    symbol.value.remove_symbol(name=index)
                # If the symbol is a DICT, remove it the key
                elif symbol.data_type == DATA_DICT:
                    symbol.value.pop(str(index))
                # If the symbol is a LIST, remove the index
                elif symbol.data_type == DATA_DICT:
                    symbol.value.pop(int(index))
                # If the symbol is any other type, then we should not be able to apply another name component to it,
                #   thus it is an error
                else:
                    raise Exception("Unsupported symbol access `" + index + "` for symbol value `" + str(
                        symbol.value) + "`. Scriptax.SymbolTable@remove_symbol")
            else:
                # If the name has no more components, we have already found the symbol we want to remove
                scope.remove_symbol(symbol=symbol)
        except:
            raise Exception("Removing existing symbol failed. Scriptax.SymbolTable@remove_symbol")


    def execute(self, name: str, parameters: List[Parameter] = None, isolated_scope: bool = False):
        """
        Executes a method by getting the method body, and its appropriate static parent and birthing a scope for the method to operate within
        Returns the method body
        """

        # Ensures that the method symbol exists
        if not self.has_symbol(name) and self.has_symbol(name, SYMBOL_MODULE):
            raise Exception(
                "Cannot execute `" + name + "` as it does not exist within scope. Scriptax.SymbolTable@execute")

        # Breaks apart the name into the scope name and the method name
        # The scope name is everything before the method name
        name = self.make_and_verify_name(name)

        # Get the scope accessing name which is everything but the last component of the name
        scope_name = name[:-1]

        # If scope_name only contains an up_word, then clear out the scope_name entirely
        if len(scope_name) == 1 and self.name_has_up(scope_name):
            scope_name = []

        # Get the Method name which is just the last component of the name
        method_name = name[-1]

        # These two lines are not needed, but are left in for readabilities sake
        instance_scope: SymbolScope = None  # This is the scope where the method is defined
        method_scope: SymbolScope = None  # This is the scope which will be used to execute the method

        # If there is a scope_name, we must be operating on an instance
        # If there is no scope_name, then we must be trying to call a function on our own instance
        if len(scope_name) > 0:
            # Attempts to find the symbol on instances
            try:
                instance_scope = self.get_symbol(name=".".join(scope_name))
            except:
                # If we cant find an instance with the name, then try and see if we have imported this name
                if not self.name_has_up(scope_name):
                    scope_name.insert(0, self.up_words[0])
                instance_scope = self.get_symbol(name=".".join(scope_name), type=SYMBOL_MODULE)

        else:
            instance_scope = self._get_parent_module()

        # Gets the method symbol from the scope
        tbl = create_table(instance_scope)
        try:
            method: Symbol = tbl.get_symbol(name=method_name, as_value=False)
        except:
            raise Exception("Method `" + ".".join(name) + "` does not exist. Scriptax.SymbolTable@execute")

        if method.data_type != DATA_METHOD:
            raise Exception("Cannot execute non executable data type `" + method.data_type + "`. Scriptax.SymbolTable@execute")

        # Spawns an anonymous scope if this should be executed in isolation, otherwise use the existing
        #   static scope
        if isolated_scope:
            method_scope = SymbolTable(name=method_name + "_isolated_method", type=SCOPE_BLOCK).scope()
        else:
            # Births a new scope for the method body inside of its static parent scope
            instance_table: SymbolTable = create_generic_table(instance_scope)
            method_scope: SymbolScope = instance_table.birth_scope(name=method_name + "_method")

        # Adds each parameter into the method scope
        if parameters:
            for parameter in parameters:
                method_scope.insert_symbol(Symbol(name=parameter.name, value=parameter.value))

        # Sets up the dynamic links from the currently executing code to the called method
        self.call(method_scope)

        # Returns the body method such that some parser or compiler can execute its body
        return method.value


    def complete_execution(self):
        """
        Completes execution
        """
        self.exit_scope()


    def new(self, name : str, path : str) -> Symbol:
        """
        No parameters on this one as it is handled via the constructor
        After calling this, use the returned scope symbol to parse the file
        """
        import_table = SymbolTable(name=name + "_import")
        return self.scope().insert_symbol(
            Symbol(name=name, symbol_type=SYMBOL_MODULE, value=import_table.scope(), attributes={"path": path}))


    def _get_import(self, name : str) -> Symbol:
        """
        Finds an import and returns it's symbol
        If it does not exist, it will throw an exception.
        """

        # Checks if a script has been imported with this name
        if not self.has_symbol(name : str, type : str =SYMBOL_MODULE):
            # Perhaps it is in the parent module scope, let's try
            up_name = self.up_words[0] + "." + name
            if not self.has_symbol(up_name, type=SYMBOL_MODULE):
                raise Exception(
                    "Cannot find symbol with name `" + name + "` to create instance from. Scriptax.SymbolTable@copy")
            else:
                name = up_name

        # If we imported module exists, then return the symbol for it
        return self.get_symbol(name, type=SYMBOL_MODULE, as_value=False)


    def copy(self, import_name : str, var_name : str) -> Symbol:
        """
        Uses the import to generate a fresh object of that type
        After calling this, use the returned scope symbol to parse the file and call the constructor
        """

        # If we imported module exists, then get the symbol for it
        symbol: Symbol = self._get_import(import_name)

        # Generate a fresh symbol table for the new instance
        instance_table = SymbolTable(name=var_name + "_instance")

        # Create a symbol for the new instance scope and attach the imported script path so that we re-parse it
        return self.scope().insert_symbol(
            Symbol(name=var_name, value=instance_table.scope(), attributes={"path": symbol.attributes['path']}))


    def extends(self, import_name : str) -> 'ExtendedImport':
        """
        Extends the current scope by an imported scope.
        Returns the SymbolTable of the extended scope (the copy of the imported scope) in order to parse using it
        """

        # If we imported module exists, then get the symbol for it
        symbol: Symbol = self._get_import(import_name)

        # Generate a fresh symbol table for the new instance
        instance_table = SymbolTable(name=import_name + "_extended_instance")

        # Injects the extended scope into the static link chain
        self.scope().extends(instance_table.scope())

        # Returns the import symbol so that we have the path to re-parse as well as the
        #   symbol table to parse with
        return ExtendedImport(sym_import=symbol, table_extended=instance_table)
    

    def implements(self, import_name : str):
        """
        Implements static method symbols from the imported scope into this scope
        """

        # If we imported module exists, then get the symbol for it
        symbol: Symbol = self._get_import(import_name)

        # Get the symbols inside of the imported module symbol and loop through them
        for sym in symbol.value.symbols:
            # Used for getting type hints in IDE
            sym: Symbol = sym

            # If the symbol is a static method, then we need to add it to our current module scope
            if sym.data_type == DATA_METHOD and 'static' in sym.attributes and sym.attributes['static'] == True: 
                self.scope().insert_symbol(sym)


class ExtendedImport:
    """
    A model class used for extending scopes
    """
    def __init__(self, sym_import: Symbol, table_extended: SymbolTable):
        self.sym_import: Symbol = sym_import
        self.table: SymbolTable = table_extended


def create_table(scope: SymbolScope) -> SymbolTable:
    """
    A helper method for wraping a SymbolScope in a SymbolTable

    Parameters
    ----------
    scope : SymbolScope
        The symbol scope we wish to wrap around
    
    Returns
    -------
    SymbolTable
        The wrapper table for the scope
    """
    table = SymbolTable()
    table.root = scope
    table.current = scope
    return table
