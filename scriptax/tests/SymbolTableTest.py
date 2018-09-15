# Application import
from scriptax.parser.utils.BoilerPlate import standardParser, customizableParser
from scriptax.drivers.builtin.Scriptax import Scriptax

from apitaxcore.logs.Log import Log
from apitaxcore.logs.StandardLog import StandardLog
from apitaxcore.models.State import State
from apitaxcore.flow.LoadedDrivers import LoadedDrivers
from apitaxcore.drivers.Drivers import Drivers

State.log = Log(StandardLog(), logColorize=False)

State.log.log("> test")

Drivers.add("scriptax", Scriptax())
LoadedDrivers.load("scriptax")

scriptax = "from scriptax import test.testing as Tester;"
scriptax += "from scriptax import test.meow as MEOWWW;"
scriptax += "api someMethod () {log('TESTING SOME METHOD'); log(variableTest);}"
scriptax += "api paramMethod(test) {log(test);}"
scriptax += "api returnMethod() {return 'wazzup';log('THIS SHOULD NOT BE REACHABLE');}"
scriptax += "log(\"test\"); log(2+4/4); variableTest=5; variableTest='okay'; shawn=True; tristan=None; jen=0X678; if(shawn) {bob=42;log(jen); if(True) {log('help me pls');log(variableTest + 5 / 3);}} someInstance = new Tester();"
scriptax += "someInstance.setPath(path1='methods are good to go');someMethod();someInstance.getPath();someInstance.resetPath();someInstance.getPath();Tester.getPath();Tester.resetPath();MEOWWW.getPath();"
scriptax += "variableTest=5.1; if(shawn && variableTest > 5) return someInstance.addOne(num=41);"
scriptax += "paramMethod(test='no way');log(returnMethod());log(someInstance.addOne(num=5));"

visitor = customizableParser(scriptax, file='inline_program')

print('Return: ' + str(visitor[0][1]))
print()
print("===")

visitor[1].symbol_table.printTable()
