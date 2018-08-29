# System import

# Application import
from apitax.grammar.build.Ah210Lexer import Ah210Lexer
from apitax.grammar.build.Ah210Parser import Ah210Parser
from apitax.grammar.AhVisitor import AhVisitor
from apitax.utilities.Files import getPath
from apitax.ah.flow.LoadedDrivers import LoadedDrivers
from apitax.ah.models.State import State

from antlr4 import *


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

        input = InputStream(self.options.driver.getDriverScript(filepath))

        # input = FileStream(filepath)
        lexer = Ah210Lexer(input)
        stream = CommonTokenStream(lexer)
        parser = Ah210Parser(stream)
        tree = parser.prog()
        #printer = AhListener()

        visitor = AhVisitor(parameters=self.parameters, options=self.options)
        visitor.setState(file=getPath(filepath))

        return visitor.visit(tree)