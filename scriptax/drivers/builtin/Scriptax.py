from apitaxcore.flow.responses.ApitaxResponse import ApitaxResponse
from commandtax.models.Command import Command
from scriptax.drivers.Driver import Driver
from time import time
from apitaxcore.utilities.Numbers import round2str
from scriptax.flow.ScriptaxExecutor import Scriptax as ScriptaxExecutor
from apitaxcore.models.State import State


class Scriptax(Driver):
    def isDriverScriptable(self) -> bool:
        return True

    def isDriverCommandable(self) -> bool:
        return True

    def getDriverName(self) -> str:
        return 'scriptax'

    def getDriverDescription(self) -> str:
        return 'Provides a method of starting Scriptax'

    def getDriverHelpEndpoint(self) -> str:
        return 'coming soon'

    def getDriverTips(self) -> str:
        return 'I recommend using the Apitax dashboard to build your Scriptax'

    def handleDriverScript(self, command: Command) -> ApitaxResponse:

        t0 = time()

        scriptax = ScriptaxExecutor(command.parameters, command.options)

        result = scriptax.execute(command.command[0])

        executionTime = round2str(time() - t0)

        if (command.options.debug):
            State.log.log('>> Script Finished Processing in ' + executionTime + 's')
            State.log.log('')

        response = ApitaxResponse()
        response.body.add({'result': result[0][1]})
        response.body.add({'commandtax': command.command[0]})
        response.body.add({'execution-time': executionTime})

        if (result[1].isError()):
            response.body.add({'error': result[1].message})
            response.status = 500
        else:
            response.status = 200

        return response

    def handleDriverCommand(self, command: Command) -> ApitaxResponse:
        if(self.isDriverScriptable()):
            return self.handleDriverScript(command)

    def getDriverScript(self, path) -> str:
        if path == 'bob/bob.ah':
            return "from scriptax import tester.bobytest(wtf='nope') as Slurp; sig(butts='beaut'); extends(Slurp); api getSig() {log(parent.butts); Slurp.doSig(); } api doBob() {log('THIS IS THE BOBBY');log(addOne(somenum=6));} api addOne(somenum) {return addOneRecursive(num=somenum);} api addOneRecursive(num) { num += 1; if(num < 10) num = addOneRecursive(num=num); return num;}"
        return "sig(wtf='yup'); api doSig() {log(parent.wtf);} api addOne(num) { if(num > 5) return num + 1; else return num; } api getPath () {log('method in script with path: ' + parent.path);} api resetPath () {parent.path='RESET';} api setPath(path){parent.path=path;} api test () {log('testing method');} log('Received filepath: " + path + "'); path='" + path + "'; arbVal=42;"
