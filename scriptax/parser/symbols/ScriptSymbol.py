from scriptax.parser.symbols.Symbol import Symbol


class ScriptSymbol(Symbol):
    def __init__(self, name=None, symbolType=None, dataType=None, value=None, path=None, driver=None):
        super().__init__(name, symbolType, dataType, value)
        self.path =path
        self.driver = driver

    def getSymbolDebug(self):
        return super().getSymbolDebug() + ':' + self.path + ':' + self.driver.getDriverName()

