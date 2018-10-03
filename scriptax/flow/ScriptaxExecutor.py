# System import

# Application import
from scriptax.parser.utils.BoilerPlate import customizableParser
from apitaxcore.utilities.Files import getPath
from apitaxcore.flow.LoadedDrivers import LoadedDrivers
from apitaxcore.models.State import State


# Script is used to automate the execution of many commands
class Scriptax():
    def __init__(self, parameters, options):
        self.options = options
        self.parameters = parameters
        self.log = State.log

    # Begins executing the script from top to bottom & handles nested scripts
    def execute(self, filepath) -> tuple:
        if self.options.debug:
            self.log.log('>>> Opening Script: ' + filepath)
            self.log.log('')
            self.log.log('')

        if not self.options.driver:
            self.options.driver = LoadedDrivers.getDefaultDriver()

        scriptax = self.options.driver.getDriverScript(filepath)

        result = customizableParser(scriptax, parameters=self.parameters, options=self.options, file=getPath(filepath))

        return result
