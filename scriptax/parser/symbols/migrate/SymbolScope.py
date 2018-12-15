from scriptax.parser.symbols.migrate.Symbol import *
from typing import List
from typing import TypeVar
import string
import json
import random

# Required to facilitate type hinting inside of the SymbolScope class
SymbolScopeType = TypeVar("SymbolScopeType", bound="SymbolScope")

SCOPE_ROOT = "root"
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
        if not name:
            self.name = ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))
        else:
            self.name: str = name
        self.type: str = scopeType
        self.index: int = 0
        self.variableScanBlocked = False

    def setMeta(self, name=None, scopeType=SCOPE_UNKNOWN):
        if name:
            self.name = name
        self.type = scopeType

    def getScopeDebug(self):
        debug = {}
        debug['scope'] = {
            'name': str(self.name),
            'scope-type': str(self.type),
            'address': hex(id(self)).upper(),
        }
        if self.parent:
            debug['scope']['parent'] = str(self.parent.name)
        else:
            debug['scope']['parent'] = "None"
        debug['scope']['symbols'] = []
        debug['scope']['children'] = []
        for symbol in self.symbols:
            debug['scope']['symbols'].append(symbol.getSymbolDebug())
        for child in self.children:
            debug['scope']['children'].append(child.getScopeDebug())
        return debug

    def printScopeDebug(self):
        print(json.dumps(self.getScopeDebug(), indent=2))

    # When generating and using the symbol table occur in independent stages, this method is used to create new child
    # scopes or use existing ones where possible.
    def nextChild(self) -> SymbolScopeType:
        nextChild: SymbolScope = None
        if (self.index >= len(self.children)):
            nextChild = SymbolScope(parent=self)
            self.children.append(nextChild)
        else:
            nextChild = self.children[self.index]
        self.index += 1
        return nextChild

    def insertScope(self, scope: SymbolScopeType):
        scope.parent = self
        self.children.append(scope)
        self.index += 1
        return scope

    def mergeScopes(self, scope: SymbolScopeType, append=False):
        self.symbols = scope.symbols + self.symbols
        if append:
            self.children = self.children + scope.children
        else:
            self.children = scope.children + self.children
            self.index += len(scope.children)

    def resetScope(self):
        self.index = 0
        for child in self.children:
            child.resetScope()

    def addSymbol(self, symbol: Symbol):
        if (self.getSymbol(symbol.name, symbol.symbolType)):
            return False
        self.symbols.append(symbol)
        return True

    def removeSymbol(self, name, symbolType=SYMBOL_VARIABLE, dataType=None):
        symbol = self.getSymbol(name, symbolType=symbolType, dataType=dataType)
        if not symbol:
            return False
        self.symbols.remove(symbol)
        return symbol

    def getSymbol(self, name, symbolType=None, dataType=None):
        for symbol in self.symbols:
            if (symbol.name == name):
                correct = True
                if symbolType and symbol.symbolType != symbolType:
                    correct = False
                if dataType and symbol.dataType != dataType:
                    correct = False
                if correct:
                    return symbol
        return None
