from scriptax.parser.symbols.SymbolTable import SymbolTable
from scriptax.parser.symbols.Symbol import *

symbol_table = SymbolTable()

symbol_table.putSymbol(symbol=Symbol(name="globalTest", symbolType=SYMBOL_VARIABLE, value="GLOBALS ROXS"))

symbol_table.printTable()

print('===')

symbol_table.enterScope()
symbol_table.current.setMeta(name="1")

symbol_table.enterScope()
symbol_table.current.setMeta(name="1a")
symbol_table.putSymbol(symbol=Symbol(name="someVar", symbolType=SYMBOL_VARIABLE, value="my test"))

symbol_table.printTable()

symbol_table.enterScope()
symbol_table.current.setMeta(name="1a1")
symbol_table.putSymbol(symbol=Symbol(name="someVar", symbolType=SYMBOL_VARIABLE, value=10))
symbol = symbol_table.getSymbol(name="someVar")
print("######### " + str(symbol.value))
symbol_table.exitScope()

symbol_table.exitScope()

symbol_table.enterScope()
symbol_table.current.setMeta(name="1b")
symbol_table.putSymbol(symbol=Symbol(name="globalTest", symbolType=SYMBOL_VARIABLE, value=False))
symbol_table.putSymbol(symbol=Symbol(name="hexTest", symbolType=SYMBOL_VARIABLE, value="0xABCD"))
symbol_table.putSymbol(symbol=Symbol(name="listTest", symbolType=SYMBOL_VARIABLE, value=[0,1,2,3]))
symbol_table.putSymbol(symbol=Symbol(name="dictTest", symbolType=SYMBOL_VARIABLE, value={"test":"success"}))
symbol_table.putSymbol(symbol=Symbol(name="noneTest", symbolType=SYMBOL_VARIABLE, value=None))
symbol_table.exitScope()

symbol_table.exitScope()

symbol_table.printTable()






