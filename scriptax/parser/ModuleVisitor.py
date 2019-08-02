from apitaxcore.models.Options import Options

from scriptax.grammar.build.Ah5Parser import Ah5Parser as AhParser
from scriptax.parser.SymbolTable import SymbolTable

from scriptax.parser.Visitor import AhVisitor


class ModuleParser(AhVisitor):
    def __init__(self, parameters: dict = None, options: Options = None, file=None, symbol_table: SymbolTable = None):
        super().__init__(parameters, options, file, symbol_table)

    def visitProg(self, ctx: AhParser.ProgContext):
        self.visit(ctx.script_structure())

    def visitScript_structure(self, ctx: AhParser.Script_structureContext):
        self.visit(ctx.statements())

    def visitStatements(self, ctx: AhParser.StatementsContext):
        i = 0
        while ctx.statement(i):
            self.visit(ctx.statement(i))
            i += 1

    def visitStatement(self, ctx: AhParser.StatementContext):
        if ctx.non_terminated():
            self.visit(ctx.non_terminated())

    def visitNon_terminated(self, ctx: AhParser.Non_terminatedContext):
        if ctx.method_def_statement():
            self.visit(ctx.method_def_statement())
