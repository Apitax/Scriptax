from scriptax.parser.symbols.SymbolScope import SymbolScope, SCOPE_MODULE
import json


# Wrapper for managing SymbolScope Activation Record Instances (ARI)
class SymbolTable:
    def __init__(self, name=None, type=SCOPE_MODULE):
        # This is the root of the linked list of scopes
        self.root: SymbolScope = SymbolScope(scope_parent=None, type=type)

        if name:
            self.root.name = name

        # The current node within the linked list we are at during execution.
        # This is likely always going to be the tail of the list, but it does not have to be.
        self.current: SymbolScope = self.root

        # The current ARI depth
        # This can also be thought of as how many nested dynamically linked scopes there are
        #   or as the length of the linked list
        self.depth: int = 0

    # Create a Dynamic Link for a call to another scope
    # Also increases the linked list depth
    # Can be thought of as adding another known element to the linked list
    def call(self, scope: SymbolScope):
        self.current = self.scope().call(scope)
        self.depth += 1

    # Removed the Dynamic Links for a call to this scope
    # Removes the tail of the linked list
    def complete_call(self):
        self.current = self.scope().complete_call()
        self.depth -= 1

    # Creates a new anonymous scope but does not call it or enter it
    def birth_scope(self, type=None, name=None) -> SymbolScope:
        scope = self.scope().birth_scope()
        if type:
            scope.type = type
        if name:
            scope.name = name
        return scope

    # Enter into an anonymous scope
    # Useful for any block scopes like IF statements, LOOPS, or method bodies.
    def enter_scope(self, type=None, name=None) -> SymbolScope:
        self.current = self.current.enter_scope()
        self.depth += 1
        if type:
            self.current.type = type
        if name:
            self.current.name = name
        return self.scope()

    # Exit out of an anonymous scope
    # This removes this scopes and deletes all the data within it including called scopes and all symbols.
    def exit_scope(self) -> SymbolScope:
        self.current = self.current.exit_scope()
        self.depth -= 1
        return self.scope()

    # Returns the current scope node the table is pointing to.
    def scope(self) -> SymbolScope:
        return self.current

    # Returns the root scope node the table is pointing to
    # This is the start of the linked list
    def root_scope(self) -> SymbolScope:
        return self.root

    def get_table_debug(self):
        return json.dumps(self.root.get_scope_debug(), indent=2)

    def get_call_stack(self):
        return json.dumps(self.root.get_call_stack(), indent=2)

    def get_call_stack_summary(self):
        return self.root.get_call_stack_summary()

    def print_debug_table(self):
        print('>> Symbol Table <<')
        print(self.get_table_debug())
        print("Symbol Table Call Stack Depth: " + str(self.depth))

    def print_call_stack(self):
        print('>> Symbol Table Call Stack <<')
        print(self.get_call_stack())
        print("Symbol Table Call Stack Depth: " + str(self.depth))

    def print_call_stack_summary(self):
        print('>> Symbol Table Call Stack Summary <<')
        print(self.get_call_stack_summary())
        print("Symbol Table Call Stack Depth: " + str(self.depth))


def create_table(scope: SymbolScope) -> SymbolTable:
    table = SymbolTable()
    table.root = scope
    table.current = scope
    return table
