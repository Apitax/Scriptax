from scriptax.parser.SymbolTable import SymbolTable
from scriptax.parser.symbols.SymbolScope import SymbolScope, SCOPE_GLOBAL, SCOPE_MODULE
from scriptax.parser.symbols.Symbol import Symbol, DATA_METHOD

# Simulation:

# Starting program
table = SymbolTable(name="program", type=SCOPE_GLOBAL)

# Loading the .ah file as a module
table.enter_scope(name='main', type=SCOPE_MODULE)

# During the parsing of the .ah file add all of the methods as symbols including the constructor as so:
table.scope().insert_symbol(Symbol(name="construct", data_type=DATA_METHOD))

module_table = SymbolTable(name="parent_obj")
module_table.set_symbol(name="mydict", value={})
module_table.set_symbol(name="mydict.someindex", value=42)
module_table.set_symbol(name="mydict.shawn", value=["one", "two", {"three": True}])
module_table.enter_scope(name="child_obj", type=SCOPE_MODULE)
module_table.set_symbol(name="ivy", value="poison")
module_table.set_symbol(name="mydict.someindex", value=43)

# Similar to a class level variable
table.set_symbol(name="myInstance", value=module_table.scope())

# After parsing the .ah file, execute the constructor by entering an anonymous scope
table.enter_scope(name="constructor_block")

print(table.get_symbol("parent.myInstance.ivy"))
table.set_symbol("parent.myInstance.ivy", value="rufus")
print(table.get_symbol("parent.myInstance.ivy"))
print(table.get_symbol("parent.myInstance.mydict"))
table.set_symbol("parent.myInstance.mydict.someindex", value=83)
print(table.get_symbol("parent.myInstance.mydict"))






#print(table.get_symbol(name="mydict.shawn.2.three"))


table.print_debug_table()
print()
table.print_call_stack()
print()
table.print_call_stack_summary()

print()
#instance_table.print_debug_table()
