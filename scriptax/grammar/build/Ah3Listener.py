# Generated from src/Ah3.g4 by ANTLR 4.7.2
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .Ah3Parser import Ah3Parser
else:
    from Ah3Parser import Ah3Parser

# This class defines a complete listener for a parse tree produced by Ah3Parser.
class Ah3Listener(ParseTreeListener):

    # Enter a parse tree produced by Ah3Parser#prog.
    def enterProg(self, ctx:Ah3Parser.ProgContext):
        pass

    # Exit a parse tree produced by Ah3Parser#prog.
    def exitProg(self, ctx:Ah3Parser.ProgContext):
        pass


    # Enter a parse tree produced by Ah3Parser#script_structure.
    def enterScript_structure(self, ctx:Ah3Parser.Script_structureContext):
        pass

    # Exit a parse tree produced by Ah3Parser#script_structure.
    def exitScript_structure(self, ctx:Ah3Parser.Script_structureContext):
        pass


    # Enter a parse tree produced by Ah3Parser#global_statements.
    def enterGlobal_statements(self, ctx:Ah3Parser.Global_statementsContext):
        pass

    # Exit a parse tree produced by Ah3Parser#global_statements.
    def exitGlobal_statements(self, ctx:Ah3Parser.Global_statementsContext):
        pass


    # Enter a parse tree produced by Ah3Parser#root_level_statements.
    def enterRoot_level_statements(self, ctx:Ah3Parser.Root_level_statementsContext):
        pass

    # Exit a parse tree produced by Ah3Parser#root_level_statements.
    def exitRoot_level_statements(self, ctx:Ah3Parser.Root_level_statementsContext):
        pass


    # Enter a parse tree produced by Ah3Parser#statements.
    def enterStatements(self, ctx:Ah3Parser.StatementsContext):
        pass

    # Exit a parse tree produced by Ah3Parser#statements.
    def exitStatements(self, ctx:Ah3Parser.StatementsContext):
        pass


    # Enter a parse tree produced by Ah3Parser#statement.
    def enterStatement(self, ctx:Ah3Parser.StatementContext):
        pass

    # Exit a parse tree produced by Ah3Parser#statement.
    def exitStatement(self, ctx:Ah3Parser.StatementContext):
        pass


    # Enter a parse tree produced by Ah3Parser#terminated.
    def enterTerminated(self, ctx:Ah3Parser.TerminatedContext):
        pass

    # Exit a parse tree produced by Ah3Parser#terminated.
    def exitTerminated(self, ctx:Ah3Parser.TerminatedContext):
        pass


    # Enter a parse tree produced by Ah3Parser#non_terminated.
    def enterNon_terminated(self, ctx:Ah3Parser.Non_terminatedContext):
        pass

    # Exit a parse tree produced by Ah3Parser#non_terminated.
    def exitNon_terminated(self, ctx:Ah3Parser.Non_terminatedContext):
        pass


    # Enter a parse tree produced by Ah3Parser#execute_statement.
    def enterExecute_statement(self, ctx:Ah3Parser.Execute_statementContext):
        pass

    # Exit a parse tree produced by Ah3Parser#execute_statement.
    def exitExecute_statement(self, ctx:Ah3Parser.Execute_statementContext):
        pass


    # Enter a parse tree produced by Ah3Parser#expr.
    def enterExpr(self, ctx:Ah3Parser.ExprContext):
        pass

    # Exit a parse tree produced by Ah3Parser#expr.
    def exitExpr(self, ctx:Ah3Parser.ExprContext):
        pass


    # Enter a parse tree produced by Ah3Parser#assignment.
    def enterAssignment(self, ctx:Ah3Parser.AssignmentContext):
        pass

    # Exit a parse tree produced by Ah3Parser#assignment.
    def exitAssignment(self, ctx:Ah3Parser.AssignmentContext):
        pass


    # Enter a parse tree produced by Ah3Parser#flow.
    def enterFlow(self, ctx:Ah3Parser.FlowContext):
        pass

    # Exit a parse tree produced by Ah3Parser#flow.
    def exitFlow(self, ctx:Ah3Parser.FlowContext):
        pass


    # Enter a parse tree produced by Ah3Parser#create_instance.
    def enterCreate_instance(self, ctx:Ah3Parser.Create_instanceContext):
        pass

    # Exit a parse tree produced by Ah3Parser#create_instance.
    def exitCreate_instance(self, ctx:Ah3Parser.Create_instanceContext):
        pass


    # Enter a parse tree produced by Ah3Parser#method_statement.
    def enterMethod_statement(self, ctx:Ah3Parser.Method_statementContext):
        pass

    # Exit a parse tree produced by Ah3Parser#method_statement.
    def exitMethod_statement(self, ctx:Ah3Parser.Method_statementContext):
        pass


    # Enter a parse tree produced by Ah3Parser#method_call.
    def enterMethod_call(self, ctx:Ah3Parser.Method_callContext):
        pass

    # Exit a parse tree produced by Ah3Parser#method_call.
    def exitMethod_call(self, ctx:Ah3Parser.Method_callContext):
        pass


    # Enter a parse tree produced by Ah3Parser#if_statement.
    def enterIf_statement(self, ctx:Ah3Parser.If_statementContext):
        pass

    # Exit a parse tree produced by Ah3Parser#if_statement.
    def exitIf_statement(self, ctx:Ah3Parser.If_statementContext):
        pass


    # Enter a parse tree produced by Ah3Parser#while_statement.
    def enterWhile_statement(self, ctx:Ah3Parser.While_statementContext):
        pass

    # Exit a parse tree produced by Ah3Parser#while_statement.
    def exitWhile_statement(self, ctx:Ah3Parser.While_statementContext):
        pass


    # Enter a parse tree produced by Ah3Parser#for_statement.
    def enterFor_statement(self, ctx:Ah3Parser.For_statementContext):
        pass

    # Exit a parse tree produced by Ah3Parser#for_statement.
    def exitFor_statement(self, ctx:Ah3Parser.For_statementContext):
        pass


    # Enter a parse tree produced by Ah3Parser#each_statement.
    def enterEach_statement(self, ctx:Ah3Parser.Each_statementContext):
        pass

    # Exit a parse tree produced by Ah3Parser#each_statement.
    def exitEach_statement(self, ctx:Ah3Parser.Each_statementContext):
        pass


    # Enter a parse tree produced by Ah3Parser#condition.
    def enterCondition(self, ctx:Ah3Parser.ConditionContext):
        pass

    # Exit a parse tree produced by Ah3Parser#condition.
    def exitCondition(self, ctx:Ah3Parser.ConditionContext):
        pass


    # Enter a parse tree produced by Ah3Parser#block.
    def enterBlock(self, ctx:Ah3Parser.BlockContext):
        pass

    # Exit a parse tree produced by Ah3Parser#block.
    def exitBlock(self, ctx:Ah3Parser.BlockContext):
        pass


    # Enter a parse tree produced by Ah3Parser#callback.
    def enterCallback(self, ctx:Ah3Parser.CallbackContext):
        pass

    # Exit a parse tree produced by Ah3Parser#callback.
    def exitCallback(self, ctx:Ah3Parser.CallbackContext):
        pass


    # Enter a parse tree produced by Ah3Parser#callback_block.
    def enterCallback_block(self, ctx:Ah3Parser.Callback_blockContext):
        pass

    # Exit a parse tree produced by Ah3Parser#callback_block.
    def exitCallback_block(self, ctx:Ah3Parser.Callback_blockContext):
        pass


    # Enter a parse tree produced by Ah3Parser#optional_parameters_block.
    def enterOptional_parameters_block(self, ctx:Ah3Parser.Optional_parameters_blockContext):
        pass

    # Exit a parse tree produced by Ah3Parser#optional_parameters_block.
    def exitOptional_parameters_block(self, ctx:Ah3Parser.Optional_parameters_blockContext):
        pass


    # Enter a parse tree produced by Ah3Parser#sig_parameter_block.
    def enterSig_parameter_block(self, ctx:Ah3Parser.Sig_parameter_blockContext):
        pass

    # Exit a parse tree produced by Ah3Parser#sig_parameter_block.
    def exitSig_parameter_block(self, ctx:Ah3Parser.Sig_parameter_blockContext):
        pass


    # Enter a parse tree produced by Ah3Parser#sig_parameter.
    def enterSig_parameter(self, ctx:Ah3Parser.Sig_parameterContext):
        pass

    # Exit a parse tree produced by Ah3Parser#sig_parameter.
    def exitSig_parameter(self, ctx:Ah3Parser.Sig_parameterContext):
        pass


    # Enter a parse tree produced by Ah3Parser#call_parameter.
    def enterCall_parameter(self, ctx:Ah3Parser.Call_parameterContext):
        pass

    # Exit a parse tree produced by Ah3Parser#call_parameter.
    def exitCall_parameter(self, ctx:Ah3Parser.Call_parameterContext):
        pass


    # Enter a parse tree produced by Ah3Parser#optional_parameter.
    def enterOptional_parameter(self, ctx:Ah3Parser.Optional_parameterContext):
        pass

    # Exit a parse tree produced by Ah3Parser#optional_parameter.
    def exitOptional_parameter(self, ctx:Ah3Parser.Optional_parameterContext):
        pass


    # Enter a parse tree produced by Ah3Parser#commandtax.
    def enterCommandtax(self, ctx:Ah3Parser.CommandtaxContext):
        pass

    # Exit a parse tree produced by Ah3Parser#commandtax.
    def exitCommandtax(self, ctx:Ah3Parser.CommandtaxContext):
        pass


    # Enter a parse tree produced by Ah3Parser#execute.
    def enterExecute(self, ctx:Ah3Parser.ExecuteContext):
        pass

    # Exit a parse tree produced by Ah3Parser#execute.
    def exitExecute(self, ctx:Ah3Parser.ExecuteContext):
        pass


    # Enter a parse tree produced by Ah3Parser#async_execute.
    def enterAsync_execute(self, ctx:Ah3Parser.Async_executeContext):
        pass

    # Exit a parse tree produced by Ah3Parser#async_execute.
    def exitAsync_execute(self, ctx:Ah3Parser.Async_executeContext):
        pass


    # Enter a parse tree produced by Ah3Parser#await_statement.
    def enterAwait_statement(self, ctx:Ah3Parser.Await_statementContext):
        pass

    # Exit a parse tree produced by Ah3Parser#await_statement.
    def exitAwait_statement(self, ctx:Ah3Parser.Await_statementContext):
        pass


    # Enter a parse tree produced by Ah3Parser#labels.
    def enterLabels(self, ctx:Ah3Parser.LabelsContext):
        pass

    # Exit a parse tree produced by Ah3Parser#labels.
    def exitLabels(self, ctx:Ah3Parser.LabelsContext):
        pass


    # Enter a parse tree produced by Ah3Parser#label_comp.
    def enterLabel_comp(self, ctx:Ah3Parser.Label_compContext):
        pass

    # Exit a parse tree produced by Ah3Parser#label_comp.
    def exitLabel_comp(self, ctx:Ah3Parser.Label_compContext):
        pass


    # Enter a parse tree produced by Ah3Parser#label.
    def enterLabel(self, ctx:Ah3Parser.LabelContext):
        pass

    # Exit a parse tree produced by Ah3Parser#label.
    def exitLabel(self, ctx:Ah3Parser.LabelContext):
        pass


    # Enter a parse tree produced by Ah3Parser#attribute.
    def enterAttribute(self, ctx:Ah3Parser.AttributeContext):
        pass

    # Exit a parse tree produced by Ah3Parser#attribute.
    def exitAttribute(self, ctx:Ah3Parser.AttributeContext):
        pass


    # Enter a parse tree produced by Ah3Parser#extends_statement.
    def enterExtends_statement(self, ctx:Ah3Parser.Extends_statementContext):
        pass

    # Exit a parse tree produced by Ah3Parser#extends_statement.
    def exitExtends_statement(self, ctx:Ah3Parser.Extends_statementContext):
        pass


    # Enter a parse tree produced by Ah3Parser#sig_statement.
    def enterSig_statement(self, ctx:Ah3Parser.Sig_statementContext):
        pass

    # Exit a parse tree produced by Ah3Parser#sig_statement.
    def exitSig_statement(self, ctx:Ah3Parser.Sig_statementContext):
        pass


    # Enter a parse tree produced by Ah3Parser#options_statement.
    def enterOptions_statement(self, ctx:Ah3Parser.Options_statementContext):
        pass

    # Exit a parse tree produced by Ah3Parser#options_statement.
    def exitOptions_statement(self, ctx:Ah3Parser.Options_statementContext):
        pass


    # Enter a parse tree produced by Ah3Parser#delete_statement.
    def enterDelete_statement(self, ctx:Ah3Parser.Delete_statementContext):
        pass

    # Exit a parse tree produced by Ah3Parser#delete_statement.
    def exitDelete_statement(self, ctx:Ah3Parser.Delete_statementContext):
        pass


    # Enter a parse tree produced by Ah3Parser#error_statement.
    def enterError_statement(self, ctx:Ah3Parser.Error_statementContext):
        pass

    # Exit a parse tree produced by Ah3Parser#error_statement.
    def exitError_statement(self, ctx:Ah3Parser.Error_statementContext):
        pass


    # Enter a parse tree produced by Ah3Parser#return_statement.
    def enterReturn_statement(self, ctx:Ah3Parser.Return_statementContext):
        pass

    # Exit a parse tree produced by Ah3Parser#return_statement.
    def exitReturn_statement(self, ctx:Ah3Parser.Return_statementContext):
        pass


    # Enter a parse tree produced by Ah3Parser#auth_statement.
    def enterAuth_statement(self, ctx:Ah3Parser.Auth_statementContext):
        pass

    # Exit a parse tree produced by Ah3Parser#auth_statement.
    def exitAuth_statement(self, ctx:Ah3Parser.Auth_statementContext):
        pass


    # Enter a parse tree produced by Ah3Parser#endpoint_statement.
    def enterEndpoint_statement(self, ctx:Ah3Parser.Endpoint_statementContext):
        pass

    # Exit a parse tree produced by Ah3Parser#endpoint_statement.
    def exitEndpoint_statement(self, ctx:Ah3Parser.Endpoint_statementContext):
        pass


    # Enter a parse tree produced by Ah3Parser#import_statement.
    def enterImport_statement(self, ctx:Ah3Parser.Import_statementContext):
        pass

    # Exit a parse tree produced by Ah3Parser#import_statement.
    def exitImport_statement(self, ctx:Ah3Parser.Import_statementContext):
        pass


    # Enter a parse tree produced by Ah3Parser#casting.
    def enterCasting(self, ctx:Ah3Parser.CastingContext):
        pass

    # Exit a parse tree produced by Ah3Parser#casting.
    def exitCasting(self, ctx:Ah3Parser.CastingContext):
        pass


    # Enter a parse tree produced by Ah3Parser#log.
    def enterLog(self, ctx:Ah3Parser.LogContext):
        pass

    # Exit a parse tree produced by Ah3Parser#log.
    def exitLog(self, ctx:Ah3Parser.LogContext):
        pass


    # Enter a parse tree produced by Ah3Parser#count.
    def enterCount(self, ctx:Ah3Parser.CountContext):
        pass

    # Exit a parse tree produced by Ah3Parser#count.
    def exitCount(self, ctx:Ah3Parser.CountContext):
        pass


    # Enter a parse tree produced by Ah3Parser#reflection.
    def enterReflection(self, ctx:Ah3Parser.ReflectionContext):
        pass

    # Exit a parse tree produced by Ah3Parser#reflection.
    def exitReflection(self, ctx:Ah3Parser.ReflectionContext):
        pass


    # Enter a parse tree produced by Ah3Parser#inject.
    def enterInject(self, ctx:Ah3Parser.InjectContext):
        pass

    # Exit a parse tree produced by Ah3Parser#inject.
    def exitInject(self, ctx:Ah3Parser.InjectContext):
        pass


    # Enter a parse tree produced by Ah3Parser#atom.
    def enterAtom(self, ctx:Ah3Parser.AtomContext):
        pass

    # Exit a parse tree produced by Ah3Parser#atom.
    def exitAtom(self, ctx:Ah3Parser.AtomContext):
        pass


    # Enter a parse tree produced by Ah3Parser#atom_obj_dict.
    def enterAtom_obj_dict(self, ctx:Ah3Parser.Atom_obj_dictContext):
        pass

    # Exit a parse tree produced by Ah3Parser#atom_obj_dict.
    def exitAtom_obj_dict(self, ctx:Ah3Parser.Atom_obj_dictContext):
        pass


    # Enter a parse tree produced by Ah3Parser#atom_obj_list.
    def enterAtom_obj_list(self, ctx:Ah3Parser.Atom_obj_listContext):
        pass

    # Exit a parse tree produced by Ah3Parser#atom_obj_list.
    def exitAtom_obj_list(self, ctx:Ah3Parser.Atom_obj_listContext):
        pass


    # Enter a parse tree produced by Ah3Parser#atom_string.
    def enterAtom_string(self, ctx:Ah3Parser.Atom_stringContext):
        pass

    # Exit a parse tree produced by Ah3Parser#atom_string.
    def exitAtom_string(self, ctx:Ah3Parser.Atom_stringContext):
        pass


    # Enter a parse tree produced by Ah3Parser#atom_number.
    def enterAtom_number(self, ctx:Ah3Parser.Atom_numberContext):
        pass

    # Exit a parse tree produced by Ah3Parser#atom_number.
    def exitAtom_number(self, ctx:Ah3Parser.Atom_numberContext):
        pass


    # Enter a parse tree produced by Ah3Parser#atom_boolean.
    def enterAtom_boolean(self, ctx:Ah3Parser.Atom_booleanContext):
        pass

    # Exit a parse tree produced by Ah3Parser#atom_boolean.
    def exitAtom_boolean(self, ctx:Ah3Parser.Atom_booleanContext):
        pass


    # Enter a parse tree produced by Ah3Parser#atom_hex.
    def enterAtom_hex(self, ctx:Ah3Parser.Atom_hexContext):
        pass

    # Exit a parse tree produced by Ah3Parser#atom_hex.
    def exitAtom_hex(self, ctx:Ah3Parser.Atom_hexContext):
        pass


    # Enter a parse tree produced by Ah3Parser#atom_none.
    def enterAtom_none(self, ctx:Ah3Parser.Atom_noneContext):
        pass

    # Exit a parse tree produced by Ah3Parser#atom_none.
    def exitAtom_none(self, ctx:Ah3Parser.Atom_noneContext):
        pass


