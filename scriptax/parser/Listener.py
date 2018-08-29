import sys
from antlr4 import *
from apitax.grammar.build.Ah2Parser import Ah2Parser
from apitax.grammar.build.Ah2Listener import Ah2Listener as Ah2ListenerOriginal


class AhListener(Ah2ListenerOriginal):
    # Enter a parse tree produced by Ah2Parser#prog.
    def enterProg(self, ctx):
        print('prog entered')
        print(ctx)

    # Exit a parse tree produced by Ah2Parser#prog.
    def exitProg(self, ctx):
        print('prog left')
        print(ctx)

    # Enter a parse tree produced by Ah2Parser#statements.
    def enterStatements(self, ctx):
        print('statements entered')
        print(ctx)

    # Exit a parse tree produced by Ah2Parser#statements.
    def exitStatements(self, ctx):
        print('statements left')
        print(ctx)

    # Enter a parse tree produced by Ah2Parser#statement.
    def enterStatement(self, ctx):
        print('statement entered')
        print(ctx)

    # Exit a parse tree produced by Ah2Parser#statement.
    def exitStatement(self, ctx):
        print('statement left')
        print(ctx)

    # Enter a parse tree produced by Ah2Parser#r.
    def enterR(self, ctx):  #:Ah2Parser.RContext):
        print('r entered')
        print(ctx.INT())

    # Exit a parse tree produced by Ah2Parser#r.
    def exitR(self, ctx):
        print('r left')
        print(ctx)