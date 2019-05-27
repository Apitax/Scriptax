from scriptax.grammar.build.Ah3Lexer import Ah3Lexer
from scriptax.grammar.build.Ah3Parser import Ah3Parser
from scriptax.parser.Visitor import AhVisitor

from antlr4 import *
from typing import Tuple, Any


def standardParser(scriptax: str) -> Tuple[Any, AhVisitor]:
    """ 
    Executes Scriptax

    Parameters
    ----------
    scriptax : str
        The scriptax code to execute

    Returns
    -------
    tuple
        The first index is the result returned, and the second index is the visitor class used for executing the script
    """
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


def customizableParser(scriptax: str, symbol_table=None, file=None, parameters=None, options=None) -> Tuple[Any, AhVisitor]:
    """ 
    Executes Scriptax

    Parameters
    ----------
    scriptax : str
        The scriptax code to execute
    symbol_table : SymbolTable, optional
        The symbol table to start with while parsing
    file : str, optional
        The name of the file we are parsing
    parameters : dict, optional
        The parameters to use when executing. Typically, method parameters, constructor parameters, etc.
    options : Options, optional
        Application options such as debug mode

    Returns
    -------
    tuple
        The first index is the result returned, and the second index is the visitor class used for executing the script
    """
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


def standardContextParser(context) -> Tuple[Any, AhVisitor]:
    """ 
    Executes an Antlr4 context

    Parameters
    ----------
    context: Antlr4Context
        This is the Antlr4 ctx variable for the block of code we wish to execute on

    Returns
    -------
    tuple
        The first index is the result returned, and the second index is the visitor class used for executing the script
    """
    visitor = AhVisitor()
    result = visitor.visit(context)
    return result, visitor


def customizableContextParser(context, symbol_table=None, file=None, parameters=None, options=None) -> Tuple[Any, AhVisitor]:
    """ 
    Executes an Antlr4 context

    Parameters
    ----------
    context: Antlr4Context
        This is the Antlr4 ctx variable for the block of code we wish to execute on

    Returns
    -------
    tuple
        The first index is the result returned, and the second index is the visitor class used for executing the script
    """
    visitor = AhVisitor(symbol_table=symbol_table, file=file, parameters=parameters, options=options)
    result = visitor.visit(context)
    return result, visitor
