from scriptax.parser.symbols.Symbol import Symbol


class SymbolScope:
    def __init__(self, name=None):
        self.symbols = []
        self.name = name

    def addSymbol(self, symbol: Symbol):
        if(self.getSymbol(symbol.name, symbol.symbolType)):
            return False
        self.symbols.append(symbol)
        return True
    
    def removeSymbol(self, symbol: Symbol):
        symbol = self.getSymbol(symbol.name, symbol.symbolType)
        if(not symbol):
            return False
        self.symbols.remove(symbol)
        
    def getSymbol(self, name, symbolType=None):
        for symbol in self.symbols:
            if(symbol.name == name):
                if(not symbolType):
                    return symbol
                else:
                    if(symbol.symbolType == symbolType):
                        return symbol
        return None  
                    
