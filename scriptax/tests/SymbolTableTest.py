# Application import
from scriptax.parser.utils.BoilerPlate import standardParser
from apitaxcore.logs.Log import Log
from apitaxcore.logs.StandardLog import StandardLog
from apitaxcore.models.State import State

from antlr4 import *


State.log = Log(StandardLog())

State.log.log("> test")

scriptax = "log(\"test\"); log(2+4/4); variableTest=5; variableTest='okay'; shawn=True; tristan=None; jen=0X678; if(shawn) {bob=42;log(jen); if(True) {log('help me pls');log(variableTest + 5 / 3);}}"

visitor = standardParser(scriptax)

print("===")

visitor.symbol_table.printTable()
