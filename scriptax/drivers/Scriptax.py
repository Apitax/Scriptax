from apitax.ah.flow.responses.ApitaxResponse import ApitaxResponse
from apitax.ah.models.Command import Command
from apitax.drivers.Driver import Driver
from time import time
from apitax.utilities.Numbers import round2str
from apitax.ah.scriptax.Scriptax import Scriptax as ScriptaxExecutor
from apitax.ah.models.State import State


class Scriptax(Driver):
    def isDriverScriptable(self) -> bool:
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

        parser = scriptax.execute(command.command[0])

        executionTime = round2str(time() - t0)

        if (command.options.debug):
            State.log.log('>> Script Finished Processing in ' + executionTime + 's')
            State.log.log('')

        response = ApitaxResponse()
        response.body.add({'result': parser.data.getStore()})
        response.body.add({'commandtax': command.command[0]})
        response.body.add({'execution-time': executionTime})

        if (parser.isError()):
            response.body.add({'error': parser.data.getError()})
            response.status = 500
        else:
            response.status = 200

        return response

    def getDriverScript(self, path) -> str:
        return "log('Received filepath: " + path + "');"
