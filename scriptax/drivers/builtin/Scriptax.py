from apitaxcore.flow.responses.ApitaxResponse import ApitaxResponse
from commandtax.models.Command import Command
from scriptax.drivers.Driver import Driver
from time import time
from apitaxcore.utilities.Numbers import round2str
from scriptax.flow.ScriptaxExecutor import Scriptax as ScriptaxExecutor
from apitaxcore.models.State import State
from scriptax.parser.utils.BoilerPlate import read_file
from pathlib import Path
from antlr4 import InputStream


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

        if command.options.debug:
            State.log.log('>> Script Finished Processing in ' + executionTime + 's')
            State.log.log('')

        response = ApitaxResponse()
        response.body.add({'result': result[0][1]})
        response.body.add({'commandtax': command.command[0]})
        response.body.add({'execution-time': executionTime})

        if result[1].is_error():
            response.body.add({'error': result[1].message})
            response.status = 500
        else:
            response.status = 200

        return response

    def handleDriverCommand(self, command: Command) -> ApitaxResponse:
        if self.isDriverScriptable():
            return self.handleDriverScript(command)

    def getDriverScript(self, path: str) -> InputStream:
        path = Path(Path(__file__).resolve().parents[2]).joinpath('tests', 'scriptax', path)
        return read_file(path)
