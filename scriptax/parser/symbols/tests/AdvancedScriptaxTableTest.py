from scriptax.parser.SymbolTable import SymbolTable, ExtendedImport, create_table
from scriptax.parser.symbols.SymbolScope import SymbolScope, SCOPE_GLOBAL, SCOPE_MODULE
from scriptax.parser.symbols.Symbol import Symbol, DATA_METHOD

# Simulation:

# Starting program
table = SymbolTable(name="program", type=SCOPE_GLOBAL)

# Loading the .ah file as a module
table.enter_scope(name='main', type=SCOPE_MODULE)


# During the parsing of the .ah file we find an import statement
# Importing std.strings which imports & extends std.base.module
module = table.new(name="strings", path="std.strings")
module_table = create_table(module.value)
module_table.new(name="basemodule", path="std.base.module")
extended: ExtendedImport = module_table.extends("basemodule")

# This is part of std.base.module
extended.table.set_symbol(name="mydict", value={})
extended.table.set_symbol(name="mydict.someindex", value=42)
extended.table.set_symbol(name="mydict.shawn", value=["one", "two", {"three": True}])
extended.table.scope().insert_symbol(Symbol(name="get_value", data_type=DATA_METHOD, value="this is a static instance method from the parent class"))

# This is part of std.strings
module_table.set_symbol(name="ivy", value="poison")
module_table.set_symbol(name="mydict.someindex", value=43)
module_table.scope().insert_symbol(Symbol(name="get_value2", data_type=DATA_METHOD, value="this is a static instance method from the child class"))

# During the parsing of the .ah file add all of the methods as symbols including the constructor as so:
table.scope().insert_symbol(Symbol(name="construct", data_type=DATA_METHOD, value="this is my method"))
table.scope().insert_symbol(Symbol(name="explore", data_type=DATA_METHOD, value="this is the explore method"))

# Similar to a class level variable
instance = table.copy(import_name="strings", var_name="myInstance")
instance = create_table(instance.value)
instance.new(name="basemodule", path="std.base.module")
extended: ExtendedImport = instance.extends("basemodule")

# This is part of std.base.module
extended.table.set_symbol(name="mydict", value={})
extended.table.set_symbol(name="mydict.someindex", value=52)
extended.table.set_symbol(name="mydict.shawn", value=["one", "two", {"three": True}])
extended.table.scope().insert_symbol(Symbol(name="get_value", data_type=DATA_METHOD, value="this is a class level instance method from the parent class"))

# This is part of std.strings
instance.set_symbol(name="ivy", value="rufus")
instance.set_symbol(name="mydict.someindex", value=53)
instance.scope().insert_symbol(Symbol(name="get_value2", data_type=DATA_METHOD, value="this is a class level instance method from the child class"))

# After parsing the .ah file, execute the constructor by entering an anonymous scope
method_body = table.execute(name="construct")

# Create a local instance inside of the constructor
instance = table.copy(import_name="strings", var_name="myLocalInstance")
instance = create_table(instance.value)
instance.new(name="basemodule", path="std.base.module")
extended: ExtendedImport = instance.extends("basemodule")

# This is part of std.base.module
extended.table.set_symbol(name="mydict", value={})
extended.table.set_symbol(name="mydict.someindex", value=62)
extended.table.set_symbol(name="mydict.shawn", value=["one", "two", {"three": True}])
extended.table.scope().insert_symbol(Symbol(name="get_value", data_type=DATA_METHOD, value="this is a local level instance method from the parent class"))

# This is part of std.strings
instance.set_symbol(name="ivy", value="lily")
instance.set_symbol(name="mydict.someindex", value=63)
instance.scope().insert_symbol(Symbol(name="get_value2", data_type=DATA_METHOD, value="this is a local instance method from the child class"))
instance.scope().insert_symbol(Symbol(name="get_value", data_type=DATA_METHOD, value="OVERRIDEN this is a local instance method from the child class"))


# table.complete_execution()
# table.complete_execution()

table.print_debug_table()
print()
table.print_call_stack()
print()
table.print_call_stack_summary()

print()


# print(table.get_symbol("parent.myInstance.ivy"))
# table.set_symbol("parent.myInstance.ivy", value="rufus")
# print(table.get_symbol("parent.myInstance.ivy"))

print(table.execute("explore"))
print(table.get_symbol("parent.myInstance.mydict"))
print(table.get_symbol("parent.myInstance.ivy"))
table.complete_execution()
print(table.get_symbol("myLocalInstance.mydict"))
print(table.get_symbol("myLocalInstance.ivy"))
print(table.execute("parent.myInstance.get_value2"))
table.complete_execution()
print(table.execute("parent.myInstance.get_value"))
table.complete_execution()
print(table.execute("myLocalInstance.get_value2"))
table.complete_execution()
print(table.execute("myLocalInstance.get_value"))
table.complete_execution()
print(table.execute(name="strings.get_value2"))
table.complete_execution()
print(table.execute(name="strings.get_value"))
table.complete_execution()

# table.set_symbol("parent.myInstance.mydict.someindex", value=83)
# print(table.get_symbol("parent.myInstance.mydict"))








# This file simulates this code: