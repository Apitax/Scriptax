from scriptax.parser.symbols.SymbolScope import SymbolScope, SCOPE_MODULE
import json


class ARISymbolTable:
    """
    Wrapper for managing SymbolScope Activation Record Instances (ARI)
    Essentially simplifies working with the SymbolScope class.
    Handles pretty printing, depth calculations, calls, and scoping

    This is a generic class which should be overriden to implement language specific features

    ...

    Attributes
    ----------
    root : SymbolScope
        The root of the symbol table tree
    current : SymbolScope
        The active entry (sometimes called node or row) of the symbol table
    depth : int
        The depth of the call stack
    """
    def __init__(self, name=None, type=SCOPE_MODULE):
        # This is the root of the linked list of scopes
        self.root: SymbolScope = SymbolScope(name="main", scope_parent=None, type=type)

        if name:
            self.root.name = name

        # The current node within the linked list we are at during execution.
        # This is likely always going to be the tail of the list, but it does not have to be.
        self.current: SymbolScope = self.root

        # The current ARI depth
        # This can also be thought of as how many nested dynamically linked scopes there are
        #   or as the length of the linked list
        self.depth: int = 0


    def call(self, scope: SymbolScope):
        """
        Create a Dynamic Link for a call to another scope
        Also increases the linked list depth
        Can be thought of as adding another known element to the linked list
        """
        self.current = self.scope().call(scope)
        self.depth += 1


    def complete_call(self):
        """
        Removed the Dynamic Links for a call to this scope
        Removes the tail of the linked list
        """
        self.current = self.scope().complete_call()
        self.depth -= 1


    def birth_scope(self, type=None, name=None) -> SymbolScope:
        """
        Creates a new anonymous scope but does not call it or enter it
        """
        scope = self.scope().birth_scope()
        if type:
            scope.type = type
        if name:
            scope.name = name
        return scope


    def enter_scope(self, type=None, name=None) -> SymbolScope:
        """
        Enter into an anonymous scope
        Useful for any block scopes like IF statements, LOOPS, or method bodies.
        """
        self.current = self.current.enter_scope()
        self.depth += 1
        if type:
            self.current.type = type
        if name:
            self.current.name = name
        return self.scope()


    def exit_scope(self) -> SymbolScope:
        """
        Exit out of an anonymous scope
        This removes this scopes and deletes all the data within it including called scopes and all symbols.
        """
        self.current = self.current.exit_scope()
        self.depth -= 1
        return self.scope()

    def scope(self) -> SymbolScope:
        """
        Returns the current scope node the table is pointing to.
        """
        return self.current


    def root_scope(self) -> SymbolScope:
        """
        Returns the root scope node the table is pointing to
        This is the start of the linked list
        """
        return self.root

    def get_table_debug(self):
        """
        Returns information about the symbol table
        """
        return json.dumps(self.root.get_scope_debug(), indent=2)

    def get_call_stack(self):
        """
        Returns the call stack of the program
        """
        return json.dumps(self.root.get_call_stack(), indent=2)

    def get_call_stack_summary(self):
        """
        Returns the call stack summary of the program
        """
        return self.root.get_call_stack_summary()

    def print_debug_table(self):
        """
        Pretty prints the symbol table information
        """
        print('>> Symbol Table <<')
        print(self.get_table_debug())
        print("Symbol Table Call Stack Depth: " + str(self.depth))

    def print_call_stack(self):
        """
        Pretty prints the call stack information
        """
        print('>> Symbol Table Call Stack <<')
        print(self.get_call_stack())
        print("Symbol Table Call Stack Depth: " + str(self.depth))

    def print_call_stack_summary(self):
        """
        Pretty prints the call stack summary information
        """
        print('>> Symbol Table Call Stack Summary <<')
        print(self.get_call_stack_summary())
        print("Symbol Table Call Stack Depth: " + str(self.depth))


def create_table(scope: SymbolScope) -> ARISymbolTable:
    """
    Creates a new symbol table given a SymbolScope

    Parameters
    ----------
    scope : SymbolScope
        The symbol scope we wish to wrap around
    
    Returns
    -------
    ARISymbolTable
        The wrapper table for the scope
    """
    table = ARISymbolTable()
    table.root = scope
    table.current = scope
    return table
