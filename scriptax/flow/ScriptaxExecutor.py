# System import

# Application import
from scriptax.parser.utils.BoilerPlate import standardParser, customizableParser
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
    def execute(self, filepath):
        if (self.options.debug):
            self.log.log('>>> Opening Script: ' + filepath)
            self.log.log('')
            self.log.log('')

        if (not self.options.driver):
            self.options.driver = LoadedDrivers.getDefaultDriver()

        scriptax = self.options.driver.getDriverScript(filepath)

        result = customizableParser(scriptax, file=getPath(filepath))

        #      input = FileStream(filepath)
        # lexer = Ah3Lexer(input)
        # stream = CommonTokenStream(lexer)
        # parser = Ah3Parser(stream)
        # tree = parser.prog()
        #      printer = AhListener()

        # visitor = AhVisitor(parameters=self.parameters, options=self.options)
        # visitor.setState(file=getPath(filepath))

        return result
