from scriptax.parser.symbols.SymbolScope import SymbolScope


class SymbolTable:
    def __init__(self):
        self.table = []
        self.table.append(SymbolScope(name="global"))
        
    def getSymbol(self, name, symbolType=None):
        for scope in reversed(self.table):
            symbol = scope.getSymbol(name, symbolType)
            if(symbol):
                return symbol
        return None
        
    def isSymbolExists(self, name, symbolType=None):
        if(self.getSymbol(name, symbolType)):
            return True
        return False
        
    def getCurrentScope(self):
        return self.table[len(self.table) - 1]
        
    def getGlobalScope(self):
        return self.table[0]
        
    def popScope(self):
        return self.table.pop()
        
    def addScope(self, name=None):
        self.table.append(SymbolScope(name=name))
        
    def printSymbolTable(self):
        length = 0
        for scope in self.table:
            indent = ""
            for i in range(0, length):
                indent += "  "
            print(indent + "> " + scope.name)
            indent += "  "
            for symbol in scope.symbols:
                print(indent + "+" + symbol.name)
            length += 1
                
                
