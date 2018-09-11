from scriptax.parser.symbols.SymbolScope import SymbolScope, SCOPE_PROGRAM


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
            if (symbol):
                return symbol
            node = node.parent
        return None

    def isSymbolExists(self, name, symbolType=None):
        if (self.getSymbol(name, symbolType)):
            return True
        return False

    def getGlobalScope(self):
        return self.root

    def getCurrentScope(self):
        return self.current
