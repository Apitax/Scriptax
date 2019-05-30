from __future__ import annotations

from scriptax.grammar.build.Ah4Lexer import Ah4Lexer
from scriptax.grammar.build.Ah4Parser import Ah4Parser
from apitaxcore.models.Options import Options

from antlr4 import *
from typing import Tuple, Any, TYPE_CHECKING

if TYPE_CHECKING:
    from scriptax.parser.Visitor import AhVisitor


def read_file(filepath: str) -> FileStream:
    return FileStream(filepath)


def read_string(scriptax: str) -> InputStream:
    return InputStream(scriptax)


def generate_parse_tree(scriptax: InputStream) -> Ah4Parser.ProgContext:
    lexer = Ah4Lexer(scriptax)
    stream = CommonTokenStream(lexer)
    parser = Ah4Parser(stream)
    return parser.prog()


def standard_parser(scriptax: InputStream) -> Tuple[Any, AhVisitor]:
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
    # Avoids cyclic import errors
    from scriptax.parser.Visitor import AhVisitor

    tree = generate_parse_tree(scriptax)
    # printer = AhListener()

    visitor = AhVisitor()
    result = visitor.visit(tree)
    return result, visitor


def customizable_parser(scriptax: InputStream, symbol_table=None, file=None, parameters=None,
                        options: Options = None) -> Tuple[
    Any, AhVisitor]:
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
    # Avoids cyclic import errors
    from scriptax.parser.Visitor import AhVisitor

    tree = generate_parse_tree(scriptax)
    # printer = AhListener()

    visitor = AhVisitor(symbol_table=symbol_table, file=file, parameters=parameters, options=options)
    result = visitor.visit(tree)
    return result, visitor


def standard_context_parser(context: ParserRuleContext) -> Tuple[Any, AhVisitor]:
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
    # Avoids cyclic import errors
    from scriptax.parser.Visitor import AhVisitor

    visitor = AhVisitor()
    result = visitor.visit(context)
    return result, visitor


def customizable_context_parser(context: ParserRuleContext, symbol_table=None, file=None, parameters=None,
                                options: Options = None) -> Tuple[Any, AhVisitor]:
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
    # Avoids cyclic import errors
    from scriptax.parser.Visitor import AhVisitor

    visitor = AhVisitor(symbol_table=symbol_table, file=file, parameters=parameters, options=options)
    result = visitor.visit(context)
    return result, visitor


def standard_tree_parser(tree: Ah4Parser.ProgContext) -> Tuple[Any, AhVisitor]:
    """
    Executes a parse tree
    This is just an alias function

    Parameters
    ----------
    tree : Ah4Parser.ProgContext
        The parse tree to execute

    Returns
    -------
    tuple
        The first index is the result returned, and the second index is the visitor class used for executing the script
    """

    return standard_context_parser(tree)


def customizable_tree_parser(tree: Ah4Parser.ProgContext, symbol_table=None, file=None, parameters=None,
                             options: Options = None) -> Tuple[Any, AhVisitor]:
    """
    Executes a parse tree
    This is just an alias function

    Parameters
    ----------
    tree : Ah4Parser.ProgContext
        The parse tree to execute
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

    return customizable_context_parser(tree, symbol_table=symbol_table, file=file, parameters=parameters,
                                       options=options)
