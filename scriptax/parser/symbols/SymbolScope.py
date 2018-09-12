from scriptax.parser.symbols.Symbol import *
from typing import List
from typing import TypeVar
import string
import random

SymbolScopeType = TypeVar("SymbolScopeType", bound="SymbolScope")

SCOPE_PROGRAM = "program"
SCOPE_SCRIPT = "script"
SCOPE_METHOD = "method"
SCOPE_BLOCK = "block"
SCOPE_CALLBACK = "callback"
SCOPE_UNKNOWN = "unknown"


class SymbolScope:
    def __init__(self, scopeType=SCOPE_UNKNOWN, name=None, parent=None):
        self.symbols: List[Symbol] = []
        self.children: List[SymbolScope] = []
        self.parent: SymbolScope = parent
        self.name: str = name
        self.type: str = scopeType
        self.index: int = 0

    def setMeta(self, name=None, scopeType=SCOPE_UNKNOWN):
        if not name:
            self.name = ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))
        else:
            self.name = name
        self.type = scopeType

    def printScope(self):
        print('{ \n' + '   ' + str(self.name) + ":" + str(self.type))
        if(self.parent):
            print('   parent: ' + str(self.parent.name))
        for symbol in self.symbols:
            print('   + ' + symbol.name + ':' + str(symbol.symbolType) + ':' + str(symbol.dataType) + ':' + str(symbol.value))
        for child in self.children:
            child.printScope()
        print('}')

    def printScopeDebug(self):
        pass

    def nextChild(self) -> SymbolScopeType:
        nextChild: SymbolScope = None
        if (self.index >= len(self.children)):
            nextChild = SymbolScope(parent=self)
            self.children.append(nextChild)
        else:
            nextChild = self.children[self.index]
        self.index += 1
        return nextChild

    def resetScope(self):
        self.index = 0
        for child in self.children:
            child.resetScope()

    def addSymbol(self, symbol: Symbol):
        if (self.getSymbol(symbol.name, symbol.symbolType)):
            return False
        self.symbols.append(symbol)
        return True

    def removeSymbol(self,  name, symbolType=SYMBOL_VARIABLE):
        symbol = self.getSymbol(name, symbolType)
        if not symbol:
            return False
        self.symbols.remove(symbol)
        return symbol

    def getSymbol(self, name, symbolType=None):
        for symbol in self.symbols:
            if (symbol.name == name):
                if (not symbolType):
                    return symbol
                else:
                    if (symbol.symbolType == symbolType):
                        return symbol
        return None
