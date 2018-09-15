from scriptax.grammar.build.Ah3Lexer import Ah3Lexer
from scriptax.grammar.build.Ah3Parser import Ah3Parser
from scriptax.parser.Visitor import AhVisitor

from antlr4 import *


def standardParser(scriptax: str) -> tuple:
    input = InputStream(scriptax)
    # input = FileStream(filepath)
    lexer = Ah3Lexer(input)
    stream = CommonTokenStream(lexer)
    parser = Ah3Parser(stream)
    tree = parser.prog()
    # printer = AhListener()

    visitor = AhVisitor()
    result = visitor.visit(tree)
    return result, visitor


def customizableParser(scriptax: str, symbol_table=None, file=None, parameters=None, options=None) -> tuple:
    input = InputStream(scriptax)
    # input = FileStream(filepath)
    lexer = Ah3Lexer(input)
    stream = CommonTokenStream(lexer)
    parser = Ah3Parser(stream)
    tree = parser.prog()
    # printer = AhListener()

    visitor = AhVisitor(symbol_table=symbol_table, file=file, parameters=parameters, options=options)
    result = visitor.visit(tree)
    return result, visitor


def standardContextParser(context) -> tuple:
    visitor = AhVisitor()
    result = visitor.visit(context)
    return result, visitor


def customizableContextParser(context, symbol_table=None, file=None, parameters=None, options=None) -> tuple:
    visitor = AhVisitor(symbol_table=symbol_table, file=file, parameters=parameters, options=options)
    result = visitor.visit(context)
    return result, visitor
