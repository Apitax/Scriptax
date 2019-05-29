from apitaxcore.models.Options import Options

from scriptax.grammar.build.Ah4Parser import Ah4Parser as AhParser, Ah4Parser
from scriptax.parser.SymbolTable import SymbolTable
from typing import List

from scriptax.parser.Visitor import AhVisitor


class ModuleParser(AhVisitor):
    def __init__(self, parameters: dict = None, options: Options = None, file=None, symbol_table: SymbolTable = None):
        super().__init__(parameters, options, file, symbol_table)

    def visitProg(self, ctx: AhParser.ProgContext):
        self.visit(ctx.script_structure())

    def visitScript_structure(self, ctx: AhParser.Script_structureContext):
        self.visit(ctx.root_level_statements())

    def visitRoot_level_statements(self, ctx: AhParser.Root_level_statementsContext):
        i = 0
        while ctx.method_def_atom(i):
            self.visit(ctx.method_def_atom(i))
            i += 1
