from scriptax.grammar.build.Ah3Lexer import Ah3Lexer

from antlr4 import *


def printLexing(scriptax: str):
    input = InputStream(scriptax)
    lexer = Ah3Lexer(input)
    for token in lexer.getAllTokens():
        print(token.text + ':' + str(token.type))
