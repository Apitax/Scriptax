from __future__ import annotations

from typing import List
from scriptax.parser.symbols.Symbol import Symbol, SYMBOL_VAR
from scriptax.utilities.Hex import instance_to_hexid

SCOPE_MODULE = 'module'
SCOPE_BLOCK = 'block'
SCOPE_GLOBAL = 'global'


class SymbolScope:
    """
    SymbolTable Activation Record Instance (ARI) class
    Contains the information necessary to get the referencing environment, as well as the calling scope and the caller scope. 
    Also contains all of the symbols associated with a scope.

    Attributes
    ----------
    type : str
        The Scope Type is mainly for debugging purposes and allows us to keep track of whether this is a block scope, a module scope, or a global scope.
    name : str
        The Scope Name is entirely for debugging purposes and allows us to add an identifier to the scope to find it more easily in debugging output.
    scope_parent : SymbolScope
        Static Link for getting the parent referencing environment for this scope.
        This should be set when the scope is first created
        Allows us to get references by using `self.`, `parent.`, `me.`, `this.` etc.
    scope_children : List[SymbolScope]
        Reverse Static Links for getting the direct children within this scopes referencing environment
        This should be updated each time that a child scope is created
        Allows us to keep track of child scopes which are accessing this referencing environment
    caller : SymbolScope
        Dynamic Link for getting the scope which called this scope and being able to return to it.
        This should be set when the scope is being executed.
        This can also be thought of as the scope table linked list parent
    calling : SymbolScope
        Reverse Dynamic Link for getting the scope which we called from this scope.
        This should be set when we call another scope to begin executing
        This can also be thought of as the scope table linked list child
    symbols : List[Symbols]
        This scopes referencing environment in the form of a list of Symbol objects
        Each time a symbol is parsed within this scope, it should be added to this list
        Symbols should not be removed from this list unless we call a delete on them
    attributes : dict
        Arbitrary attributes which can be applied to a symbol scope
    """

    def __init__(self, scope_parent, type=None, caller=None, name=''):

        self.type: str = type

        self.name = name

        self.scope_parent: SymbolScope = scope_parent

        self.scope_children: List[SymbolScope] = []

        self.caller: SymbolScope = caller

        self.calling: SymbolScope = None

        self.symbols: List[Symbol] = []

        self.attributes: dict = {}

    @staticmethod
    def conform_name(name):
        """
        Checks to see whether a symbol name is valid by removing all whitespace from it
        Removes spaces, \r, \n, \t
        Throws exception if result is an empty string, otherwise it returns the string
        """
        name = "".join(name.split())
        if len(name) < 1:
            raise Exception('Invalid symbol name `' + name + '` ' + 'Scriptax.SymbolScope@conform_name')
        else:
            return name

    def get_symbol(self, name, symbol_type=SYMBOL_VAR):
        """
        Gets symbol from this SymbolScope
        If it does not exist, throws exception
        """
        name = SymbolScope.conform_name(name)
        for symbol in self.symbols:
            if symbol.name == name and symbol.symbol_type == symbol_type:
                return symbol
        raise Exception('No symbol called `' + name + '` exists in SymbolScope. Scriptax.SymbolScope@get_symbol')

    def has_symbol(self, name, symbol_type=SYMBOL_VAR):
        """
        Checks whether this SymbolScope has a symbol
        """
        name = SymbolScope.conform_name(name)
        try:
            self.get_symbol(name, symbol_type)
        except:
            return False
        return True

    def insert_symbol(self, symbol: Symbol) -> Symbol:
        """
        Inserts a Symbol into this SymbolScope
        If a Symbol already exists with the same name, throws exception
        """
        symbol.name = SymbolScope.conform_name(symbol.name)
        if self.has_symbol(symbol.name, symbol.symbol_type):
            raise Exception(
                'SymbolScope already contains symbol `' + symbol.name + '` and cannot insert a new one. Scriptax.SymbolScope@insert_symbol')
        self.symbols.append(symbol)
        return symbol

    def remove_symbol(self, name=None, symbol_type=SYMBOL_VAR, symbol: Symbol = None):
        """
        Remove a Symbol from this SymbolScope
        If a Symbol cannot be removed, throws exception
        """
        if not name and not symbol:
            raise Exception('Must specify either s symbol or a name to remove a symbol')
        if not name:
            name = symbol.name
            symbol_type = symbol.symbol_type
        try:
            name = SymbolScope.conform_name(name)
            symbol = self.get_symbol(name, symbol_type=symbol_type)
            self.symbols.remove(symbol)
        except:
            raise Exception(
                'Unable to remove Symbol called `' + name + '` from this SymbolScope. Scriptax.SymbolScope@remove_symbol')

    def add_child_scope(self, scope):
        """
        Adds a child scope to this referencing environment
        Example 1: if this scope were of a module, a child scope might be a method declared within it
        Example 2: if this scope were for an IF statement, a child scope might be a loop declared within it
        """
        self.scope_children.append(scope)

    def remove_child_scope(self, scope):
        """
        Removes a child scope from this referencing environment
        Example: if this scope were of an IF statement with a child scope for a LOOP, after the LOOP completes we would want to remove the LOOP scope from the IF statements child scopes
        This is not relevant if this scope is a module as it would be unlikely that we would want to remove a child scope in that case
        """
        self.scope_children.remove(scope)

    def disown_scope(self):
        """
        Cleans up Static and Dynamic Reverse Links as well as the Dynamic Link
        Wipes the Symbol list
        """
        for scope in self.scope_children:
            scope.disown_scope()

        self.scope_parent.remove_child_scope(self)
        self.caller = None
        self.calling = None
        self.symbols = []

    def called(self, scope):
        """
        Creates the Dynamic Link to the scope which executed a call on this scope
        Similar to the SymbolTable linked list parent
        Used when a pre-existing and known scope is being exited
        To use an anonymous scope, use exit_scope
        """
        self.caller = scope

    def call(self, scope):
        """
        Creates the Reverse Dynamic Link to another scope when we execute a call
        Similar to the SymbolTable linked list child
        Used when a pre-existing and known scope is being entered
        To use an anonymous scope, use enter_scope
        """
        self.calling = scope
        self.calling.called(self)
        return self.calling

    def complete_call(self):
        """
        Signals to the caller that this scope has finished executing its call
        Cleans up Dynamic Link
        """
        self.caller.call_complete()
        parent_scope = self.caller
        self.caller = None
        return parent_scope

    def call_complete(self):
        """
        Cleans up the scope after a call is completed
        In other words, cleans up Reverse Dynamic Link
        """
        self.calling = None

    def birth_scope(self):
        """
        Creates an anonymous block scope
        Handles the static linking
        """
        scope = SymbolScope(scope_parent=self, type=SCOPE_BLOCK)
        self.add_child_scope(scope)
        return scope

    def enter_scope(self):
        """
        Creates an anonymous scope and calls it
        Indirectly handles the static and dynamic linking
        """
        scope = self.birth_scope()
        return self.call(scope)

    def exit_scope(self):
        """
        Exits this scope and returns the parent scope
        Cleans up all of the linking and symbols as well
        """
        parent_scope = self.complete_call()
        self.disown_scope()
        return parent_scope

    def extends(self, scope: SymbolScope):
        """
        Injects a static scope between this scope and its parent
        Handles all of the static linking
        So if the static linking looks like: A->B->C and we want to call extends on C with a scope called D it would become: A->B->D->C
        This does not touch dynamic links
        """

        # May not necessarily have a parent if we are extending the top level scope
        if self.scope_parent:
            # Unlinks the parent scope from this scope
            self.scope_parent.remove_child_scope(self)
            # Links the parent scope to the new scope
            self.scope_parent.add_child_scope(scope)
            # Links the new scope to the parent scope
            scope.scope_parent = self.scope_parent
        # Links the new scope to this scope
        scope.add_child_scope(self)
        # Links this scope to the new scope
        self.scope_parent = scope

    def get_scope_debug(self):
        """
        Returns information about the scope
        """
        debug = {
            'scope': {
                'name': str(self.name),
                'scope-type': str(self.type),
                'address': instance_to_hexid(self),
                'attributes': self.attributes,
                'symbols': [],
                'dynamic_links': {"caller": {}, "calling": {}},
                'static_links': {"parent": {}, "children": []},
            }
        }
        if self.scope_parent:
            debug['scope']['static_links']['parent'] = {
                "name": str(self.scope_parent.name),
                "address": instance_to_hexid(self.scope_parent)
            }

        if self.caller:
            debug['scope']['dynamic_links']['caller'] = {
                "name": str(self.caller.name),
                "address": instance_to_hexid(self.caller)
            }

        if self.calling:
            debug['scope']['dynamic_links']['calling'] = {
                "name": str(self.calling.name),
                "address": instance_to_hexid(self.calling)
            }

        for symbol in self.symbols:
            debug['scope']['symbols'].append(symbol.get_symbol_debug())

        for child in self.scope_children:
            debug['scope']['static_links']['children'].append(child.get_scope_debug())

        return debug

    def get_call_stack(self):
        """
        Returns the current call stack
        """
        stack = {
            'scope': {
                'name': str(self.name),
                'scope-type': str(self.type),
                'address': instance_to_hexid(self),
                'symbols': [],
                'scope_parent': {},
                'caller': {},
                'calling': {},
            }
        }

        for symbol in self.symbols:
            stack['scope']['symbols'].append(symbol.get_symbol_debug())

        if self.scope_parent:
            stack['scope']['scope_parent'] = {
                "name": str(self.scope_parent.name),
                "address": instance_to_hexid(self.scope_parent)
            }

        if self.caller:
            stack['scope']['caller'] = {
                "name": str(self.caller.name),
                "address": instance_to_hexid(self.caller)
            }

        if self.calling:
            stack['scope']['calling'] = self.calling.get_call_stack()

        return stack

    def get_call_stack_summary(self) -> str:
        """
        Returns the current call stack in short form
        """
        stack = str(self.name) + "(" + str(self.type) + ":" + instance_to_hexid(self) + ")"
        if self.calling:
            stack += " -> " + self.calling.get_call_stack_summary()
        return stack

    def print_scope_debug(self):
        """
        Prints the scope debug information
        """
        print(self.get_scope_debug())

    def print_call_stack(self):
        """
        Prints the call stack information
        """
        print(self.get_call_stack())

    def print_call_stack_summary(self):
        """
        Prints the call stack summary information
        """
        print(self.get_call_stack_summary())
