# Application import
from scriptax.grammar.build.Ah3Lexer import Ah3Lexer
from scriptax.grammar.build.Ah3Parser import Ah3Parser
from scriptax.parser.Visitor import AhVisitor
from apitaxcore.logs.Log import Log
from apitaxcore.logs.StandardLog import StandardLog
from apitaxcore.models.State import State

from antlr4 import *


State.log = Log(StandardLog())

State.log.log("> test")

scriptax = "log(\"test\"); log(2+4/4); variableTest=5; variableTest='okay'; shawn=True; tristan=None; jen='0X678'; if(shawn) {bob=42;log(jen); if(True) {log('help me pls');}}"

input = InputStream(scriptax)

# input = FileStream(filepath)
lexer = Ah3Lexer(input)
stream = CommonTokenStream(lexer)
parser = Ah3Parser(stream)
tree = parser.prog()
# printer = AhListener()

visitor = AhVisitor()
visitor.visit(tree)

print("===")

visitor.symbol_table.printTable()
