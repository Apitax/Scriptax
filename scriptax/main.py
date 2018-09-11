from scriptax.parser.symbols.SymbolTable import SymbolTable
from scriptax.parser.symbols.Symbol import *

symbol_table = SymbolTable()

symbol_table.printTable()

print('===')

symbol_table.enterScope()
symbol_table.current.setMeta(name="1")

symbol_table.enterScope()
symbol_table.current.setMeta(name="1a")
symbol_table.current.addSymbol(symbol=Symbol(name="someVar", symbolType=SYMBOL_VARIABLE, dataType=DATA_STRING, value="my test"))

symbol_table.enterScope()
symbol_table.current.setMeta(name="1a1")
symbol = symbol_table.getSymbol(name="someVar")
symbol.value = "best test"
print("######### " + symbol.value)
symbol_table.exitScope()

symbol_table.exitScope()

symbol_table.enterScope()
symbol_table.current.setMeta(name="1b")

symbol_table.exitScope()

symbol_table.exitScope()

symbol_table.printTable()






