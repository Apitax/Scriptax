# Generated from /home/shawn/Documents/projects/Apitax/Scriptax/scriptax/grammar/src/Ah5.g4 by ANTLR 4.7.2
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .Ah5Parser import Ah5Parser
else:
    from Ah5Parser import Ah5Parser

# This class defines a complete generic visitor for a parse tree produced by Ah5Parser.

class Ah5Visitor(ParseTreeVisitor):

    # Visit a parse tree produced by Ah5Parser#prog.
    def visitProg(self, ctx:Ah5Parser.ProgContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Ah5Parser#script_structure.
    def visitScript_structure(self, ctx:Ah5Parser.Script_structureContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Ah5Parser#global_statements.
    def visitGlobal_statements(self, ctx:Ah5Parser.Global_statementsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Ah5Parser#statements.
    def visitStatements(self, ctx:Ah5Parser.StatementsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Ah5Parser#statement.
    def visitStatement(self, ctx:Ah5Parser.StatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Ah5Parser#expr.
    def visitExpr(self, ctx:Ah5Parser.ExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Ah5Parser#atom.
    def visitAtom(self, ctx:Ah5Parser.AtomContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Ah5Parser#terminated.
    def visitTerminated(self, ctx:Ah5Parser.TerminatedContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Ah5Parser#runnable_statements.
    def visitRunnable_statements(self, ctx:Ah5Parser.Runnable_statementsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Ah5Parser#non_terminated.
    def visitNon_terminated(self, ctx:Ah5Parser.Non_terminatedContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Ah5Parser#method_call_statement.
    def visitMethod_call_statement(self, ctx:Ah5Parser.Method_call_statementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Ah5Parser#each_statement.
    def visitEach_statement(self, ctx:Ah5Parser.Each_statementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Ah5Parser#atom_callback.
    def visitAtom_callback(self, ctx:Ah5Parser.Atom_callbackContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Ah5Parser#callback_block.
    def visitCallback_block(self, ctx:Ah5Parser.Callback_blockContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Ah5Parser#method_def_atom.
    def visitMethod_def_atom(self, ctx:Ah5Parser.Method_def_atomContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Ah5Parser#method_def_statement.
    def visitMethod_def_statement(self, ctx:Ah5Parser.Method_def_statementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Ah5Parser#flow.
    def visitFlow(self, ctx:Ah5Parser.FlowContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Ah5Parser#if_statement.
    def visitIf_statement(self, ctx:Ah5Parser.If_statementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Ah5Parser#for_statement.
    def visitFor_statement(self, ctx:Ah5Parser.For_statementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Ah5Parser#until_statement.
    def visitUntil_statement(self, ctx:Ah5Parser.Until_statementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Ah5Parser#while_statement.
    def visitWhile_statement(self, ctx:Ah5Parser.While_statementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Ah5Parser#switch_statement.
    def visitSwitch_statement(self, ctx:Ah5Parser.Switch_statementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Ah5Parser#case_statement.
    def visitCase_statement(self, ctx:Ah5Parser.Case_statementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Ah5Parser#default_statement.
    def visitDefault_statement(self, ctx:Ah5Parser.Default_statementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Ah5Parser#range_function.
    def visitRange_function(self, ctx:Ah5Parser.Range_functionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Ah5Parser#block.
    def visitBlock(self, ctx:Ah5Parser.BlockContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Ah5Parser#done_statement.
    def visitDone_statement(self, ctx:Ah5Parser.Done_statementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Ah5Parser#continue_statement.
    def visitContinue_statement(self, ctx:Ah5Parser.Continue_statementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Ah5Parser#os_statement.
    def visitOs_statement(self, ctx:Ah5Parser.Os_statementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Ah5Parser#log_statement.
    def visitLog_statement(self, ctx:Ah5Parser.Log_statementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Ah5Parser#flexible_parameter_block.
    def visitFlexible_parameter_block(self, ctx:Ah5Parser.Flexible_parameter_blockContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Ah5Parser#flexible_parameter.
    def visitFlexible_parameter(self, ctx:Ah5Parser.Flexible_parameterContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Ah5Parser#import_statement.
    def visitImport_statement(self, ctx:Ah5Parser.Import_statementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Ah5Parser#extends_statement.
    def visitExtends_statement(self, ctx:Ah5Parser.Extends_statementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Ah5Parser#atom_create_instance.
    def visitAtom_create_instance(self, ctx:Ah5Parser.Atom_create_instanceContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Ah5Parser#ahoptions_statement.
    def visitAhoptions_statement(self, ctx:Ah5Parser.Ahoptions_statementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Ah5Parser#optional_parameters_block.
    def visitOptional_parameters_block(self, ctx:Ah5Parser.Optional_parameters_blockContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Ah5Parser#optional_parameter.
    def visitOptional_parameter(self, ctx:Ah5Parser.Optional_parameterContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Ah5Parser#dict_signal.
    def visitDict_signal(self, ctx:Ah5Parser.Dict_signalContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Ah5Parser#casting.
    def visitCasting(self, ctx:Ah5Parser.CastingContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Ah5Parser#assignment_statement.
    def visitAssignment_statement(self, ctx:Ah5Parser.Assignment_statementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Ah5Parser#data_type.
    def visitData_type(self, ctx:Ah5Parser.Data_typeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Ah5Parser#atom_obj_dict.
    def visitAtom_obj_dict(self, ctx:Ah5Parser.Atom_obj_dictContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Ah5Parser#dict_comp.
    def visitDict_comp(self, ctx:Ah5Parser.Dict_compContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Ah5Parser#atom_obj_list.
    def visitAtom_obj_list(self, ctx:Ah5Parser.Atom_obj_listContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Ah5Parser#atom_obj_enum.
    def visitAtom_obj_enum(self, ctx:Ah5Parser.Atom_obj_enumContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Ah5Parser#error_statement.
    def visitError_statement(self, ctx:Ah5Parser.Error_statementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Ah5Parser#inject.
    def visitInject(self, ctx:Ah5Parser.InjectContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Ah5Parser#condition.
    def visitCondition(self, ctx:Ah5Parser.ConditionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Ah5Parser#return_statement.
    def visitReturn_statement(self, ctx:Ah5Parser.Return_statementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Ah5Parser#typing.
    def visitTyping(self, ctx:Ah5Parser.TypingContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Ah5Parser#count.
    def visitCount(self, ctx:Ah5Parser.CountContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Ah5Parser#delete_statement.
    def visitDelete_statement(self, ctx:Ah5Parser.Delete_statementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Ah5Parser#await_statement.
    def visitAwait_statement(self, ctx:Ah5Parser.Await_statementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Ah5Parser#reflection.
    def visitReflection(self, ctx:Ah5Parser.ReflectionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Ah5Parser#required_parameter.
    def visitRequired_parameter(self, ctx:Ah5Parser.Required_parameterContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Ah5Parser#labels.
    def visitLabels(self, ctx:Ah5Parser.LabelsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Ah5Parser#label_comp.
    def visitLabel_comp(self, ctx:Ah5Parser.Label_compContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Ah5Parser#label.
    def visitLabel(self, ctx:Ah5Parser.LabelContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Ah5Parser#attributes.
    def visitAttributes(self, ctx:Ah5Parser.AttributesContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Ah5Parser#atom_string.
    def visitAtom_string(self, ctx:Ah5Parser.Atom_stringContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Ah5Parser#atom_number.
    def visitAtom_number(self, ctx:Ah5Parser.Atom_numberContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Ah5Parser#atom_boolean.
    def visitAtom_boolean(self, ctx:Ah5Parser.Atom_booleanContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Ah5Parser#atom_hex.
    def visitAtom_hex(self, ctx:Ah5Parser.Atom_hexContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Ah5Parser#atom_none.
    def visitAtom_none(self, ctx:Ah5Parser.Atom_noneContext):
        return self.visitChildren(ctx)



del Ah5Parser