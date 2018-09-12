from scriptax.grammar.build.Ah3Lexer import Ah3Lexer
from scriptax.grammar.build.Ah3Parser import Ah3Parser
from scriptax.parser.Visitor import AhVisitor

from antlr4 import *


def standardParser(scriptax: str) -> AhVisitor:
    input = InputStream(scriptax)
    # input = FileStream(filepath)
    lexer = Ah3Lexer(input)
    stream = CommonTokenStream(lexer)
    parser = Ah3Parser(stream)
    tree = parser.prog()
    # printer = AhListener()

    visitor = AhVisitor()
    visitor.visit(tree)
    return visitor
