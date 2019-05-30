from scriptax.parser.Visitor import AhVisitor
from apitaxcore.models.Options import Options

from apitaxcore.logs.Log import Log
from apitaxcore.logs.StandardLog import StandardLog
from apitaxcore.models.State import State

from scriptax.models.Attributes import Attributes
from scriptax.parser.SymbolTable import SymbolTable, create_table
from scriptax.parser.symbols.SymbolScope import SymbolScope, SCOPE_GLOBAL, SCOPE_MODULE
from scriptax.parser.symbols.Symbol import Symbol, DATA_METHOD

State.log = Log(StandardLog(), logColorize=False)
State.log.log("")
State.log.log("> Running TestVisitorSymbolTable\n\n")

visitor = AhVisitor(parameters=[], options=Options(debug=True))

visitor.symbol_table.enter_scope(name='main', type=SCOPE_MODULE)

visitor.import_module_string("strings", "script static testing() {log('test');} flinstones=42;")
visitor.import_module_string("bigstrings", "script testing() {log('test: ' + self.flinstones);} flinstones=42;")

# visitor.new_instance("bigstrings")

visitor.execute_method("strings.testing", parameters=[])

instance = visitor.new_instance(import_name="bigstrings")
visitor.set_variable("bob", instance)
visitor.execute_method("bob.testing", parameters=[])
print(visitor.get_variable("bob.flinstones"))

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

visitor.register_method("construct", method_context=None, attributes=Attributes())

visitor.execute_method("self.construct", parameters=[])


visitor.symbol_table.print_debug_table()
print()
visitor.symbol_table.print_call_stack()
print()
visitor.symbol_table.print_call_stack_summary()
print()

visitor.symbol_table.complete_execution()
visitor.symbol_table.print_call_stack_summary()
print()
