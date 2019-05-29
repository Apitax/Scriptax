from scriptax.parser.Visitor import AhVisitor

from scriptax.parser.SymbolTable import SymbolTable, ExtendedImport, create_table
from scriptax.parser.symbols.SymbolScope import SymbolScope, SCOPE_GLOBAL, SCOPE_MODULE
from scriptax.parser.symbols.Symbol import Symbol, DATA_METHOD


visitor = AhVisitor(parameters=[])

visitor.symbol_table.enter_scope(name='main', type=SCOPE_MODULE)

# visitor.import_module_string("strings", "script testing() {}")
visitor.import_module_string("bigstrings", "")

# visitor.new_instance("bigstrings")

visitor.set_variable("foo", "bar")

visitor.set_variable("pina", "colada")

print(visitor.get_variable("foo"))

visitor.set_variable("foo", "foo")

print(visitor.get_variable("foo"))

visitor.delete_variable("foo")

try:
    print(visitor.get_variable("foo"))
except:
    print("There is no foo")

visitor.register_method("construct", body_context=None, static=False)

visitor.execute_method("construct", parameters=[])


visitor.symbol_table.print_debug_table()
print()
visitor.symbol_table.print_call_stack()
print()
visitor.symbol_table.print_call_stack_summary()
print()

visitor.symbol_table.complete_execution()
visitor.symbol_table.print_call_stack_summary()
print()
