from scriptax.parser.symbols.migrate.SymbolScope import SymbolScope, SCOPE_PROGRAM, SCOPE_SCRIPT
from scriptax.parser.symbols.migrate.Symbol import *
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

    def traverseToParent(self, name=None, start: SymbolScope=None) -> tuple:
        if start:
            node: SymbolScope = start
        else:
            node: SymbolScope = self.current
        i = 0
        comps = name.split('.')
        while len(comps) > 0 and comps[0] == 'parent':
            while node.type != SCOPE_SCRIPT:
                node = node.parent
                if not node:
                    return None, None, None
            i += 1
            del comps[0]
        # Ignore the rest of comps because we only want to retrieve the
        #   symbol and leave the rest of the dots for the logic
        if len(comps) > 0:
            name = comps[0]
        else:
            name = None
        return node, name, i

    def getSymbol(self, name, symbolType=None):
        return self.getSymbolWithLength(name, symbolType)[0]

    # Returns the symbol and the number of components used out of the name label
    def getSymbolWithLength(self, name, symbolType=None) -> tuple:
        node, name, i = self.traverseToParent(name=name)
        while node is not None:
            symbol = node.getSymbol(name, symbolType)
            if symbol:
                return symbol, i
            if symbolType == SYMBOL_VARIABLE and node.variableScanBlocked:
                return None, None
            node = node.parent
        return None, None

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

    def getAt(self, name, symbolType=None) -> tuple:
        node, name, i = self.traverseToParent(name=name)
        if not name:
            return node, i
        while node is not None:
            symbol = node.getSymbol(name, symbolType)
            if symbol:
                return symbol, i
            if symbolType == SYMBOL_VARIABLE and node.variableScanBlocked:
                return None, None
            node = node.parent
        return None, None

    def deleteSymbol(self, name, symbolType=SYMBOL_VARIABLE):
        node, name, i = self.traverseToParent(name=name)
        # node: SymbolScope = self.current
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

