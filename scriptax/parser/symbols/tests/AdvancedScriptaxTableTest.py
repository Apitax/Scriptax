from scriptax.parser.SymbolTable import SymbolTable, ExtendedImport, create_table
from scriptax.parser.symbols.SymbolScope import SymbolScope, SCOPE_GLOBAL, SCOPE_MODULE
from scriptax.parser.symbols.Symbol import Symbol, DATA_METHOD

# Simulation:

### STARTING THE PROGRAM

# Starting program
table = SymbolTable(name="program", type=SCOPE_GLOBAL)

### BEGIN TO PARSE THE ENTRY POINT FILE

# Loading the .ah file as a module
table.enter_scope(name='main', type=SCOPE_MODULE)

### PARSE THE IMPORTS INSIDE OF THE ENTRY POINT FILE

# During the parsing of the .ah file we find an import statement
# Importing std.strings which imports & extends std.base.ah.module
module = table.new(name="strings", path="std.strings")
module_table = create_table(module.value)
module_table.new(name="basemodule", path="std.base.ah.module") # The strings class extends std.base.ah.module
extended: ExtendedImport = module_table.extends("basemodule") # Inside of std.strings.ah, this would be like parsing the line: extend basemodule;

# This is part of std.base.ah.module
# When importing strings, the class we are importing is a class which extends this class
extended.table.set_symbol(name="mydict", value={})
extended.table.set_symbol(name="mydict.someindex", value=42)
extended.table.set_symbol(name="mydict.shawn", value=["one", "two", {"three": True}])
extended.table.scope().insert_symbol(Symbol(name="get_value", data_type=DATA_METHOD, value="this is a static instance method from the parent class", attributes={'static': True}))

# This is part of std.strings
# After completing the std.base.ah.module extension of strings, we find other symbols and methods inside of the string class
module_table.set_symbol(name="ivy", value="poison")
module_table.set_symbol(name="mydict.someindex", value=43)
module_table.scope().insert_symbol(Symbol(name="get_value2", data_type=DATA_METHOD, value="this is a static instance method from the child class", attributes={'static': True}))

### PARSE THE EXTENDS PART OF THE ENTRY FILE

# During the parsing of the .ah file we find an extends with strings statement
# Inside of the entry point file, this would be like parsing: extend with strings;
table.implements(import_name="strings")

### PARSE THE OPTIONS PART OF THE ENTRY FILE
# For now nothing is here

### PARSE THE METHODS INSIDE OF THE ENTRY POINT FILE

# During the parsing of the .ah file add all of the methods as symbols including the constructor as so:
table.scope().insert_symbol(Symbol(name="construct", data_type=DATA_METHOD, value="this is my method"))
table.scope().insert_symbol(Symbol(name="explore", data_type=DATA_METHOD, value="this is the explore method"))

### PARSE THE CLASS LEVEL VARIABLES OF THE ENTRY POINT FILE

# Similar to a class level variable
instance = table.copy(import_name="strings", var_name="myInstance")
instance = create_table(instance.value)
instance.new(name="basemodule", path="std.base.ah.module") # The strings class extends std.base.ah.module
extended: ExtendedImport = instance.extends("basemodule")

# This is part of std.base.ah.module
# When creating the class level variable, the instance we are creating is a class which extends this class
extended.table.set_symbol(name="mydict", value={})
extended.table.set_symbol(name="mydict.someindex", value=52)
extended.table.set_symbol(name="mydict.shawn", value=["one", "two", {"three": True}])
extended.table.scope().insert_symbol(Symbol(name="get_value", data_type=DATA_METHOD, value="this is a class level instance method from the parent class"))

# This is part of std.strings
# After completing the std.base.ah.module extension of strings, we find other symbols and methods inside of the string class
instance.set_symbol(name="ivy", value="rufus")
instance.set_symbol(name="mydict.someindex", value=53)
instance.scope().insert_symbol(Symbol(name="get_value2", data_type=DATA_METHOD, value="this is a class level instance method from the child class"))

### PARSING OF THE ENTRY POINT FILE HAS COMPLETED
### NOW EXECUTE THE `construct` METHOD IN THE ENTRY POINT FILE. If none exists, the program will terminate. 

# After parsing the .ah file, execute the constructor by entering an anonymous scope
method_body = table.execute(name="construct")

### EXECUTE THE BLOCK OF CODE IN THE CONSTRUCTOR BODY BLOCK

# Create a local instance inside of the constructor
instance = table.copy(import_name="strings", var_name="myLocalInstance")
instance = create_table(instance.value)
instance.new(name="basemodule", path="std.base.ah.module")
extended: ExtendedImport = instance.extends("basemodule")

# This is part of std.base.ah.module
extended.table.set_symbol(name="mydict", value={})
extended.table.set_symbol(name="mydict.someindex", value=62)
extended.table.set_symbol(name="mydict.shawn", value=["one", "two", {"three": True}])
extended.table.scope().insert_symbol(Symbol(name="get_value", data_type=DATA_METHOD, value="this is a local level instance method from the parent class"))

# This is part of std.strings
instance.set_symbol(name="ivy", value="lily")
instance.set_symbol(name="mydict.someindex", value=63)
instance.scope().insert_symbol(Symbol(name="get_value2", data_type=DATA_METHOD, value="this is a local instance method from the child class"))
instance.scope().insert_symbol(Symbol(name="get_value", data_type=DATA_METHOD, value="OVERRIDEN this is a local instance method from the child class"))

### PRINT OUT SOME DEBUG STUFF AT THIS POINT IN THE EXECUTION

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
print(table.execute(name="self.construct"))
table.complete_execution()
print(table.execute(name="self.explore"))
table.complete_execution()
print(table.execute(name="self.get_value2"))
table.complete_execution()

print("deletion tests")
print(table.get_symbol("parent.myInstance.mydict.shawn"))
table.remove_symbol("parent.myInstance.mydict.shawn.1")
table.remove_symbol("parent.myInstance.mydict.someindex")
print(table.get_symbol("parent.myInstance.mydict"))


# Complete the execution of the constructor
table.complete_execution()

# Complete the execution of the entry point file
table.complete_execution()

# Program ends here, verify the call stack is empty.
print()
table.print_call_stack_summary()

# table.set_symbol("parent.myInstance.mydict.someindex", value=83)
# print(table.get_symbol("parent.myInstance.mydict"))


# This file simulates this code:


# FILE: std.base.ah.module
# mydict = {};
# mydict.someindex = 42;
# mydict.shawn = ["one", "two", {"three": true}];

# static script get_value()
# {
#     log("this is a static instance method from the parent class");
# }

# script get_value2()
# {
#     log("this is an instance method from the parent class");
# }

# =====

# FILE: std.strings
# from std.base.ah import module as basemodule;
# extend basemodule;

# ivy = "poison";
# mydict.someindex = 43;

# static script get_value()
# {
#     log("this is a static instance method from the parent class");
# }

# script get_value2()
# {
#     log("this is an instance method from the parent class");
# }

# =====

# FILE: main
# from std import strings;
# extend with strings;

# myInstance = new strings();

# script construct()
# {
#     log("this is my method");
#     myLocalInstance = new strings();

#     explore();

#     log(myLocalInstance.mydict);
#     log(myLocalInstance.ivy);

#     self.myInstace.get_value2();
#     this.myInstace.get_value();

#     myLocalInstace.get_value2();
#     myLocalInstace.get_value();

#     strings.get_value2();
#     strings.get_value();

#     self.explore();
#     self.get_value2();
# }

# script explore()
# {
#     log("this is the explore method");

#     log(parent.myInstance.mydict);
#     log(parent.myInstance.ivy);
# }
