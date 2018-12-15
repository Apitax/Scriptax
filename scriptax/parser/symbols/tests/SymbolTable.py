from scriptax.parser.symbols.SymbolTable import SymbolTable, create_table
from scriptax.parser.symbols.SymbolScope import SymbolScope, SCOPE_GLOBAL, SCOPE_MODULE
from scriptax.parser.symbols.Symbol import Symbol, DATA_METHOD

# Simulation:

# Starting program
table = SymbolTable(name="program", type=SCOPE_GLOBAL)

# Loading the .ah file as a module
table.enter_scope(name='main', type=SCOPE_MODULE)

# During the parsing of the .ah file add all of the methods as symbols including the constructor as so:
table.scope().insert_symbol(Symbol(name="construct", data_type=DATA_METHOD))

# While parsing .ah file, an instance variable declaration was found
instance_table = SymbolTable(name="myInstance")
instance_table.scope().insert_symbol(Symbol(name="getValue", data_type=DATA_METHOD))
table.scope().insert_symbol(Symbol(name="myInstance", value=instance_table.scope()))

# After parsing the .ah file, execute the constructor by entering an anonymous scope
table.enter_scope(name="constructor_block")

# Below is doing the constructor method body

# In the constructor, we execute a call to the getValue method on our myInstance variable
instance_scope: SymbolScope = table.scope().scope_parent.get_symbol(name="myInstance").value
instance_table: SymbolTable = create_table(instance_scope)
method_scope: SymbolScope = instance_table.birth_scope(name="getValue_block")
table.call(method_scope)

# And here we would begin executing the method
method = instance_scope.get_symbol(name="getValue").value

# And this is like the getValue method body

table.scope().insert_symbol(Symbol(name="myval", value=42))
table.scope().insert_symbol(Symbol(name="myval2", value=84))
symbol = table.scope().get_symbol(name="myval2")
table.scope().remove_symbol(name="myval")


# End of program
table.exit_scope()
table.exit_scope()
table.exit_scope()

table.print_debug_table()
print()
table.print_call_stack()
print()
table.print_call_stack_summary()

print()
instance_table.print_debug_table()
