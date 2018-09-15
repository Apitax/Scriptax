from scriptax.parser.symbols.SymbolScope import SymbolScope, SCOPE_PROGRAM, SCOPE_SCRIPT
from scriptax.parser.symbols.Symbol import *
import json

class SymbolTable:
    def __init__(self):
        self.root: SymbolScope = SymbolScope(scopeType=SCOPE_PROGRAM, name="global")
        self.current: SymbolScope = self.root
        self.deleteOnExit = False

    def enterScope(self):
        self.current = self.current.nextChild()

    def exitScope(self):
        temp = None
        if self.deleteOnExit:
            temp = self.current
        self.current = self.current.parent
        if self.deleteOnExit:
            self.current.children.remove(temp)

    def exitScopeAndDelete(self):
        temp = self.current
        self.current = self.current.parent
        self.current.children.remove(temp)

    def insertScope(self, scope: SymbolScope):
        self.current = self.current.insertScope(scope)

    def printTable(self):
        print('>>Symbol Table<<')
        print(json.dumps(self.root.getScopeDebug(), indent=2))

    def resetTable(self):
        self.root.resetScope()

    def printDebugScopeTree(self):
        self.root.printScopeDebug()

    def getSymbol(self, name, symbolType=None):
        node: SymbolScope = self.current

        comps = name.split('.')
        while comps[0] == 'parent' and len(comps) > 1:
            while node.type != SCOPE_SCRIPT:
                node = node.parent
                if not node:
                    return None
            del comps[0]
        name = ".".join(comps)

        while node is not None:
            symbol = node.getSymbol(name, symbolType)
            if symbol:
                return symbol
            if symbolType == SYMBOL_VARIABLE and node.variableScanBlocked:
                return None
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


def createTableFromScope(scope: SymbolScope) -> SymbolTable:
    table = SymbolTable()
    table.root = scope # TODO: This should be come the parent node until NONE
    table.current = scope
    return table

