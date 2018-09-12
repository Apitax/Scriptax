from scriptax.parser.symbols.SymbolScope import SymbolScope, SCOPE_PROGRAM
from scriptax.parser.symbols.Symbol import *


class SymbolTable:
    def __init__(self):
        self.root: SymbolScope = SymbolScope(scopeType=SCOPE_PROGRAM, name="global")
        self.current: SymbolScope = self.root

    def enterScope(self):
        self.current = self.current.nextChild()

    def exitScope(self):
        self.current = self.current.parent

    def printTable(self):
        print('>>Symbol Table<<')
        self.root.printScope()

    def resetTable(self):
        self.root.resetScope()

    def printDebugScopeTree(self):
        self.root.printScopeDebug()

    def getSymbol(self, name, symbolType=None):
        node: SymbolScope = self.current
        while node is not None:
            symbol = node.getSymbol(name, symbolType)
            if symbol:
                return symbol
            node = node.parent
        return None

    def isSymbolExists(self, name, symbolType=None):
        symbol = self.getSymbol(name, symbolType)
        if symbol:
            return symbol
        return False

    def putSymbol(self, symbol: Symbol):
        temp = self.isSymbolExists(symbol.name, symbolType=symbol.symbolType)
        if temp:
            temp.value = symbol.value
            temp.dataType = symbol.dataType
        else:
            self.current.addSymbol(symbol=symbol)

    def deleteSymbol(self, name, symbolType=SYMBOL_VARIABLE):
        node: SymbolScope = self.current
        while node is not None:
            symbol = node.removeSymbol(name, symbolType)
            if symbol:
                return symbol
            node = node.parent
        return False

    def getGlobalScope(self):
        return self.root

    def getCurrentScope(self):
        return self.current
