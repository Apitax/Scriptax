# Application import
from scriptax.parser.utils.BoilerPlate import standardParser
from scriptax.drivers.builtin.Scriptax import Scriptax

from apitaxcore.logs.Log import Log
from apitaxcore.logs.StandardLog import StandardLog
from apitaxcore.models.State import State
from apitaxcore.flow.LoadedDrivers import LoadedDrivers
from apitaxcore.drivers.Drivers import Drivers

State.log = Log(StandardLog())

State.log.log("> test")

Drivers.add("scriptax", Scriptax())
LoadedDrivers.load("scriptax")

scriptax = "from scriptax import test.testing as Tester;"
scriptax += "from scriptax import test.meow as MEOWWW;"
scriptax += "log(\"test\"); log(2+4/4); variableTest=5; variableTest='okay'; shawn=True; tristan=None; jen=0X678; if(shawn) {bob=42;log(jen); if(True) {log('help me pls');log(variableTest + 5 / 3);}} someInstance = new Tester();"

visitor = standardParser(scriptax)

print("===")

visitor.symbol_table.printTable()
