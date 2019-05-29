# Generated from src/Ah4.g4 by ANTLR 4.7.2
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .Ah4Parser import Ah4Parser
else:
    from Ah4Parser import Ah4Parser

# This class defines a complete generic visitor for a parse tree produced by Ah4Parser.

class Ah4Visitor(ParseTreeVisitor):

    # Visit a parse tree produced by Ah4Parser#prog.
    def visitProg(self, ctx:Ah4Parser.ProgContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Ah4Parser#script_structure.
    def visitScript_structure(self, ctx:Ah4Parser.Script_structureContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Ah4Parser#global_statements.
    def visitGlobal_statements(self, ctx:Ah4Parser.Global_statementsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Ah4Parser#root_level_statements.
    def visitRoot_level_statements(self, ctx:Ah4Parser.Root_level_statementsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Ah4Parser#statements.
    def visitStatements(self, ctx:Ah4Parser.StatementsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Ah4Parser#statement.
    def visitStatement(self, ctx:Ah4Parser.StatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Ah4Parser#expr.
    def visitExpr(self, ctx:Ah4Parser.ExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Ah4Parser#atom.
    def visitAtom(self, ctx:Ah4Parser.AtomContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Ah4Parser#terminated.
    def visitTerminated(self, ctx:Ah4Parser.TerminatedContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Ah4Parser#runnable_statements.
    def visitRunnable_statements(self, ctx:Ah4Parser.Runnable_statementsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Ah4Parser#method_call_statement.
    def visitMethod_call_statement(self, ctx:Ah4Parser.Method_call_statementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Ah4Parser#commandtax_statement.
    def visitCommandtax_statement(self, ctx:Ah4Parser.Commandtax_statementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Ah4Parser#os_statement.
    def visitOs_statement(self, ctx:Ah4Parser.Os_statementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Ah4Parser#each_statement.
    def visitEach_statement(self, ctx:Ah4Parser.Each_statementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Ah4Parser#atom_callback.
    def visitAtom_callback(self, ctx:Ah4Parser.Atom_callbackContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Ah4Parser#callback_block.
    def visitCallback_block(self, ctx:Ah4Parser.Callback_blockContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Ah4Parser#method_def_atom.
    def visitMethod_def_atom(self, ctx:Ah4Parser.Method_def_atomContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Ah4Parser#non_terminated.
    def visitNon_terminated(self, ctx:Ah4Parser.Non_terminatedContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Ah4Parser#flow.
    def visitFlow(self, ctx:Ah4Parser.FlowContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Ah4Parser#if_statement.
    def visitIf_statement(self, ctx:Ah4Parser.If_statementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Ah4Parser#for_statement.
    def visitFor_statement(self, ctx:Ah4Parser.For_statementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Ah4Parser#while_statement.
    def visitWhile_statement(self, ctx:Ah4Parser.While_statementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Ah4Parser#switch_statement.
    def visitSwitch_statement(self, ctx:Ah4Parser.Switch_statementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Ah4Parser#case_statement.
    def visitCase_statement(self, ctx:Ah4Parser.Case_statementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Ah4Parser#default_statement.
    def visitDefault_statement(self, ctx:Ah4Parser.Default_statementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Ah4Parser#block.
    def visitBlock(self, ctx:Ah4Parser.BlockContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Ah4Parser#done_statement.
    def visitDone_statement(self, ctx:Ah4Parser.Done_statementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Ah4Parser#continue_statement.
    def visitContinue_statement(self, ctx:Ah4Parser.Continue_statementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Ah4Parser#log_statement.
    def visitLog_statement(self, ctx:Ah4Parser.Log_statementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Ah4Parser#flexible_parameter_block.
    def visitFlexible_parameter_block(self, ctx:Ah4Parser.Flexible_parameter_blockContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Ah4Parser#flexible_parameter.
    def visitFlexible_parameter(self, ctx:Ah4Parser.Flexible_parameterContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Ah4Parser#import_statement.
    def visitImport_statement(self, ctx:Ah4Parser.Import_statementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Ah4Parser#extends_statement.
    def visitExtends_statement(self, ctx:Ah4Parser.Extends_statementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Ah4Parser#create_instance.
    def visitCreate_instance(self, ctx:Ah4Parser.Create_instanceContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Ah4Parser#ahoptions_statement.
    def visitAhoptions_statement(self, ctx:Ah4Parser.Ahoptions_statementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Ah4Parser#optional_parameters_block.
    def visitOptional_parameters_block(self, ctx:Ah4Parser.Optional_parameters_blockContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Ah4Parser#optional_parameter.
    def visitOptional_parameter(self, ctx:Ah4Parser.Optional_parameterContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Ah4Parser#dict_signal.
    def visitDict_signal(self, ctx:Ah4Parser.Dict_signalContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Ah4Parser#casting.
    def visitCasting(self, ctx:Ah4Parser.CastingContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Ah4Parser#atom_obj_dict.
    def visitAtom_obj_dict(self, ctx:Ah4Parser.Atom_obj_dictContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Ah4Parser#assignment_statement.
    def visitAssignment_statement(self, ctx:Ah4Parser.Assignment_statementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Ah4Parser#atom_obj_list.
    def visitAtom_obj_list(self, ctx:Ah4Parser.Atom_obj_listContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Ah4Parser#atom_obj_enum.
    def visitAtom_obj_enum(self, ctx:Ah4Parser.Atom_obj_enumContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Ah4Parser#error_statement.
    def visitError_statement(self, ctx:Ah4Parser.Error_statementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Ah4Parser#inject.
    def visitInject(self, ctx:Ah4Parser.InjectContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Ah4Parser#condition.
    def visitCondition(self, ctx:Ah4Parser.ConditionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Ah4Parser#return_statement.
    def visitReturn_statement(self, ctx:Ah4Parser.Return_statementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Ah4Parser#count.
    def visitCount(self, ctx:Ah4Parser.CountContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Ah4Parser#delete_statement.
    def visitDelete_statement(self, ctx:Ah4Parser.Delete_statementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Ah4Parser#await_statement.
    def visitAwait_statement(self, ctx:Ah4Parser.Await_statementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Ah4Parser#reflection.
    def visitReflection(self, ctx:Ah4Parser.ReflectionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Ah4Parser#required_parameter.
    def visitRequired_parameter(self, ctx:Ah4Parser.Required_parameterContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Ah4Parser#labels.
    def visitLabels(self, ctx:Ah4Parser.LabelsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Ah4Parser#label_comp.
    def visitLabel_comp(self, ctx:Ah4Parser.Label_compContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Ah4Parser#label.
    def visitLabel(self, ctx:Ah4Parser.LabelContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Ah4Parser#attributes.
    def visitAttributes(self, ctx:Ah4Parser.AttributesContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Ah4Parser#atom_string.
    def visitAtom_string(self, ctx:Ah4Parser.Atom_stringContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Ah4Parser#atom_number.
    def visitAtom_number(self, ctx:Ah4Parser.Atom_numberContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Ah4Parser#atom_boolean.
    def visitAtom_boolean(self, ctx:Ah4Parser.Atom_booleanContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Ah4Parser#atom_hex.
    def visitAtom_hex(self, ctx:Ah4Parser.Atom_hexContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Ah4Parser#atom_none.
    def visitAtom_none(self, ctx:Ah4Parser.Atom_noneContext):
        return self.visitChildren(ctx)



del Ah4Parser