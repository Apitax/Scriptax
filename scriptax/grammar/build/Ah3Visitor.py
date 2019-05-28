# Generated from src/Ah3.g4 by ANTLR 4.7.2
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .Ah3Parser import Ah3Parser
else:
    from Ah3Parser import Ah3Parser

# This class defines a complete generic visitor for a parse tree produced by Ah3Parser.

class Ah3Visitor(ParseTreeVisitor):

    # Visit a parse tree produced by Ah3Parser#prog.
    def visitProg(self, ctx:Ah3Parser.ProgContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Ah3Parser#script_structure.
    def visitScript_structure(self, ctx:Ah3Parser.Script_structureContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Ah3Parser#global_statements.
    def visitGlobal_statements(self, ctx:Ah3Parser.Global_statementsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Ah3Parser#root_level_statements.
    def visitRoot_level_statements(self, ctx:Ah3Parser.Root_level_statementsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Ah3Parser#statements.
    def visitStatements(self, ctx:Ah3Parser.StatementsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Ah3Parser#statement.
    def visitStatement(self, ctx:Ah3Parser.StatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Ah3Parser#terminated.
    def visitTerminated(self, ctx:Ah3Parser.TerminatedContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Ah3Parser#non_terminated.
    def visitNon_terminated(self, ctx:Ah3Parser.Non_terminatedContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Ah3Parser#execute_statement.
    def visitExecute_statement(self, ctx:Ah3Parser.Execute_statementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Ah3Parser#expr.
    def visitExpr(self, ctx:Ah3Parser.ExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Ah3Parser#assignment.
    def visitAssignment(self, ctx:Ah3Parser.AssignmentContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Ah3Parser#flow.
    def visitFlow(self, ctx:Ah3Parser.FlowContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Ah3Parser#create_instance.
    def visitCreate_instance(self, ctx:Ah3Parser.Create_instanceContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Ah3Parser#method_statement.
    def visitMethod_statement(self, ctx:Ah3Parser.Method_statementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Ah3Parser#method_call.
    def visitMethod_call(self, ctx:Ah3Parser.Method_callContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Ah3Parser#if_statement.
    def visitIf_statement(self, ctx:Ah3Parser.If_statementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Ah3Parser#while_statement.
    def visitWhile_statement(self, ctx:Ah3Parser.While_statementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Ah3Parser#for_statement.
    def visitFor_statement(self, ctx:Ah3Parser.For_statementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Ah3Parser#each_statement.
    def visitEach_statement(self, ctx:Ah3Parser.Each_statementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Ah3Parser#condition.
    def visitCondition(self, ctx:Ah3Parser.ConditionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Ah3Parser#block.
    def visitBlock(self, ctx:Ah3Parser.BlockContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Ah3Parser#callback.
    def visitCallback(self, ctx:Ah3Parser.CallbackContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Ah3Parser#callback_block.
    def visitCallback_block(self, ctx:Ah3Parser.Callback_blockContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Ah3Parser#optional_parameters_block.
    def visitOptional_parameters_block(self, ctx:Ah3Parser.Optional_parameters_blockContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Ah3Parser#sig_parameter_block.
    def visitSig_parameter_block(self, ctx:Ah3Parser.Sig_parameter_blockContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Ah3Parser#sig_parameter.
    def visitSig_parameter(self, ctx:Ah3Parser.Sig_parameterContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Ah3Parser#call_parameter.
    def visitCall_parameter(self, ctx:Ah3Parser.Call_parameterContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Ah3Parser#optional_parameter.
    def visitOptional_parameter(self, ctx:Ah3Parser.Optional_parameterContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Ah3Parser#commandtax.
    def visitCommandtax(self, ctx:Ah3Parser.CommandtaxContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Ah3Parser#execute.
    def visitExecute(self, ctx:Ah3Parser.ExecuteContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Ah3Parser#async_execute.
    def visitAsync_execute(self, ctx:Ah3Parser.Async_executeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Ah3Parser#await_statement.
    def visitAwait_statement(self, ctx:Ah3Parser.Await_statementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Ah3Parser#labels.
    def visitLabels(self, ctx:Ah3Parser.LabelsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Ah3Parser#label_comp.
    def visitLabel_comp(self, ctx:Ah3Parser.Label_compContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Ah3Parser#label.
    def visitLabel(self, ctx:Ah3Parser.LabelContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Ah3Parser#attribute.
    def visitAttribute(self, ctx:Ah3Parser.AttributeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Ah3Parser#extends_statement.
    def visitExtends_statement(self, ctx:Ah3Parser.Extends_statementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Ah3Parser#sig_statement.
    def visitSig_statement(self, ctx:Ah3Parser.Sig_statementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Ah3Parser#options_statement.
    def visitOptions_statement(self, ctx:Ah3Parser.Options_statementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Ah3Parser#delete_statement.
    def visitDelete_statement(self, ctx:Ah3Parser.Delete_statementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Ah3Parser#error_statement.
    def visitError_statement(self, ctx:Ah3Parser.Error_statementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Ah3Parser#return_statement.
    def visitReturn_statement(self, ctx:Ah3Parser.Return_statementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Ah3Parser#auth_statement.
    def visitAuth_statement(self, ctx:Ah3Parser.Auth_statementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Ah3Parser#endpoint_statement.
    def visitEndpoint_statement(self, ctx:Ah3Parser.Endpoint_statementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Ah3Parser#import_statement.
    def visitImport_statement(self, ctx:Ah3Parser.Import_statementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Ah3Parser#casting.
    def visitCasting(self, ctx:Ah3Parser.CastingContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Ah3Parser#log.
    def visitLog(self, ctx:Ah3Parser.LogContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Ah3Parser#count.
    def visitCount(self, ctx:Ah3Parser.CountContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Ah3Parser#reflection.
    def visitReflection(self, ctx:Ah3Parser.ReflectionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Ah3Parser#inject.
    def visitInject(self, ctx:Ah3Parser.InjectContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Ah3Parser#atom.
    def visitAtom(self, ctx:Ah3Parser.AtomContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Ah3Parser#atom_obj_dict.
    def visitAtom_obj_dict(self, ctx:Ah3Parser.Atom_obj_dictContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Ah3Parser#atom_obj_list.
    def visitAtom_obj_list(self, ctx:Ah3Parser.Atom_obj_listContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Ah3Parser#atom_string.
    def visitAtom_string(self, ctx:Ah3Parser.Atom_stringContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Ah3Parser#atom_number.
    def visitAtom_number(self, ctx:Ah3Parser.Atom_numberContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Ah3Parser#atom_boolean.
    def visitAtom_boolean(self, ctx:Ah3Parser.Atom_booleanContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Ah3Parser#atom_hex.
    def visitAtom_hex(self, ctx:Ah3Parser.Atom_hexContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Ah3Parser#atom_none.
    def visitAtom_none(self, ctx:Ah3Parser.Atom_noneContext):
        return self.visitChildren(ctx)



del Ah3Parser