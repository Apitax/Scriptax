# from scriptax.parser.symbols.migrate.SymbolTable import SymbolTable
# from scriptax.parser.symbols.migrate.Symbol import *

# symbol_table = SymbolTable()

# symbol_table.putSymbol(symbol=Symbol(name="globalTest", symbolType=SYMBOL_VARIABLE, value="GLOBALS ROXS"))

# symbol_table.printTable()

# print('===')

# symbol_table.enterScope()
# symbol_table.current.setMeta(name="1")

# symbol_table.enterScope()
# symbol_table.current.setMeta(name="1a")
# symbol_table.putSymbol(symbol=Symbol(name="someVar", symbolType=SYMBOL_VARIABLE, value="my test"))

# symbol_table.printTable()

# symbol_table.enterScope()
# symbol_table.current.setMeta(name="1a1")
# symbol_table.putSymbol(symbol=Symbol(name="someVar", symbolType=SYMBOL_VARIABLE, value=10))
# symbol = symbol_table.getSymbol(name="someVar")
# print("######### " + str(symbol.value))
# symbol_table.exitScope()

# symbol_table.exitScope()

# symbol_table.enterScope()
# symbol_table.current.setMeta(name="1b")
# symbol_table.putSymbol(symbol=Symbol(name="globalTest", symbolType=SYMBOL_VARIABLE, value=False))
# symbol_table.putSymbol(symbol=Symbol(name="hexTest", symbolType=SYMBOL_VARIABLE, value="0xABCD"))
# symbol_table.putSymbol(symbol=Symbol(name="listTest", symbolType=SYMBOL_VARIABLE, value=[0,1,2,3]))
# symbol_table.putSymbol(symbol=Symbol(name="dictTest", symbolType=SYMBOL_VARIABLE, value={"test":"success"}))
# symbol_table.putSymbol(symbol=Symbol(name="noneTest", symbolType=SYMBOL_VARIABLE, value=None))
# symbol_table.exitScope()

# symbol_table.exitScope()

# symbol_table.printTable()


from scriptax.parser.symbols.ARISymbolTable import ARISymbolTable, create_table
from scriptax.parser.symbols.SymbolScope import SymbolScope, SCOPE_GLOBAL, SCOPE_MODULE
from scriptax.parser.symbols.Symbol import Symbol, DATA_METHOD

# Simulation:

# Starting program
table = ARISymbolTable(name="program", type=SCOPE_GLOBAL)

# Loading the .ah file as a module
table.enter_scope(name='main', type=SCOPE_MODULE)

# During the parsing of the .ah file add all of the methods as symbols including the constructor as so:
table.scope().insert_symbol(Symbol(name="construct", data_type=DATA_METHOD))

# While parsing .ah file, an instance variable declaration was found
instance_table = ARISymbolTable(name="myInstance")
instance_table.scope().insert_symbol(Symbol(name="getValue", data_type=DATA_METHOD))
table.scope().insert_symbol(Symbol(name="myInstance", value=instance_table.scope()))

# After parsing the .ah file, execute the constructor by entering an anonymous scope
table.enter_scope(name="constructor_block")

# Below is doing the constructor method body

# In the constructor, we execute a call to the getValue method on our myInstance variable
instance_scope: SymbolScope = table.scope().scope_parent.get_symbol(name="myInstance").value
instance_table: ARISymbolTable = create_table(instance_scope)
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
#table.exit_scope()
#table.exit_scope()
#table.exit_scope()

table.print_debug_table()
print()
table.print_call_stack()
print()
table.print_call_stack_summary()

print()
instance_table.print_debug_table()




