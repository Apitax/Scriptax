# Generated from /home/shawn/Documents/projects/Apitax/Scriptax/scriptax/grammar/src/Ah5.g4 by ANTLR 4.7.2
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .Ah5Parser import Ah5Parser
else:
    from Ah5Parser import Ah5Parser

# This class defines a complete listener for a parse tree produced by Ah5Parser.
class Ah5Listener(ParseTreeListener):

    # Enter a parse tree produced by Ah5Parser#prog.
    def enterProg(self, ctx:Ah5Parser.ProgContext):
        pass

    # Exit a parse tree produced by Ah5Parser#prog.
    def exitProg(self, ctx:Ah5Parser.ProgContext):
        pass


    # Enter a parse tree produced by Ah5Parser#script_structure.
    def enterScript_structure(self, ctx:Ah5Parser.Script_structureContext):
        pass

    # Exit a parse tree produced by Ah5Parser#script_structure.
    def exitScript_structure(self, ctx:Ah5Parser.Script_structureContext):
        pass


    # Enter a parse tree produced by Ah5Parser#global_statements.
    def enterGlobal_statements(self, ctx:Ah5Parser.Global_statementsContext):
        pass

    # Exit a parse tree produced by Ah5Parser#global_statements.
    def exitGlobal_statements(self, ctx:Ah5Parser.Global_statementsContext):
        pass


    # Enter a parse tree produced by Ah5Parser#statements.
    def enterStatements(self, ctx:Ah5Parser.StatementsContext):
        pass

    # Exit a parse tree produced by Ah5Parser#statements.
    def exitStatements(self, ctx:Ah5Parser.StatementsContext):
        pass


    # Enter a parse tree produced by Ah5Parser#statement.
    def enterStatement(self, ctx:Ah5Parser.StatementContext):
        pass

    # Exit a parse tree produced by Ah5Parser#statement.
    def exitStatement(self, ctx:Ah5Parser.StatementContext):
        pass


    # Enter a parse tree produced by Ah5Parser#expr.
    def enterExpr(self, ctx:Ah5Parser.ExprContext):
        pass

    # Exit a parse tree produced by Ah5Parser#expr.
    def exitExpr(self, ctx:Ah5Parser.ExprContext):
        pass


    # Enter a parse tree produced by Ah5Parser#atom.
    def enterAtom(self, ctx:Ah5Parser.AtomContext):
        pass

    # Exit a parse tree produced by Ah5Parser#atom.
    def exitAtom(self, ctx:Ah5Parser.AtomContext):
        pass


    # Enter a parse tree produced by Ah5Parser#terminated.
    def enterTerminated(self, ctx:Ah5Parser.TerminatedContext):
        pass

    # Exit a parse tree produced by Ah5Parser#terminated.
    def exitTerminated(self, ctx:Ah5Parser.TerminatedContext):
        pass


    # Enter a parse tree produced by Ah5Parser#runnable_statements.
    def enterRunnable_statements(self, ctx:Ah5Parser.Runnable_statementsContext):
        pass

    # Exit a parse tree produced by Ah5Parser#runnable_statements.
    def exitRunnable_statements(self, ctx:Ah5Parser.Runnable_statementsContext):
        pass


    # Enter a parse tree produced by Ah5Parser#non_terminated.
    def enterNon_terminated(self, ctx:Ah5Parser.Non_terminatedContext):
        pass

    # Exit a parse tree produced by Ah5Parser#non_terminated.
    def exitNon_terminated(self, ctx:Ah5Parser.Non_terminatedContext):
        pass


    # Enter a parse tree produced by Ah5Parser#method_call_statement.
    def enterMethod_call_statement(self, ctx:Ah5Parser.Method_call_statementContext):
        pass

    # Exit a parse tree produced by Ah5Parser#method_call_statement.
    def exitMethod_call_statement(self, ctx:Ah5Parser.Method_call_statementContext):
        pass


    # Enter a parse tree produced by Ah5Parser#each_statement.
    def enterEach_statement(self, ctx:Ah5Parser.Each_statementContext):
        pass

    # Exit a parse tree produced by Ah5Parser#each_statement.
    def exitEach_statement(self, ctx:Ah5Parser.Each_statementContext):
        pass


    # Enter a parse tree produced by Ah5Parser#atom_callback.
    def enterAtom_callback(self, ctx:Ah5Parser.Atom_callbackContext):
        pass

    # Exit a parse tree produced by Ah5Parser#atom_callback.
    def exitAtom_callback(self, ctx:Ah5Parser.Atom_callbackContext):
        pass


    # Enter a parse tree produced by Ah5Parser#callback_block.
    def enterCallback_block(self, ctx:Ah5Parser.Callback_blockContext):
        pass

    # Exit a parse tree produced by Ah5Parser#callback_block.
    def exitCallback_block(self, ctx:Ah5Parser.Callback_blockContext):
        pass


    # Enter a parse tree produced by Ah5Parser#method_def_atom.
    def enterMethod_def_atom(self, ctx:Ah5Parser.Method_def_atomContext):
        pass

    # Exit a parse tree produced by Ah5Parser#method_def_atom.
    def exitMethod_def_atom(self, ctx:Ah5Parser.Method_def_atomContext):
        pass


    # Enter a parse tree produced by Ah5Parser#method_def_statement.
    def enterMethod_def_statement(self, ctx:Ah5Parser.Method_def_statementContext):
        pass

    # Exit a parse tree produced by Ah5Parser#method_def_statement.
    def exitMethod_def_statement(self, ctx:Ah5Parser.Method_def_statementContext):
        pass


    # Enter a parse tree produced by Ah5Parser#flow.
    def enterFlow(self, ctx:Ah5Parser.FlowContext):
        pass

    # Exit a parse tree produced by Ah5Parser#flow.
    def exitFlow(self, ctx:Ah5Parser.FlowContext):
        pass


    # Enter a parse tree produced by Ah5Parser#if_statement.
    def enterIf_statement(self, ctx:Ah5Parser.If_statementContext):
        pass

    # Exit a parse tree produced by Ah5Parser#if_statement.
    def exitIf_statement(self, ctx:Ah5Parser.If_statementContext):
        pass


    # Enter a parse tree produced by Ah5Parser#for_statement.
    def enterFor_statement(self, ctx:Ah5Parser.For_statementContext):
        pass

    # Exit a parse tree produced by Ah5Parser#for_statement.
    def exitFor_statement(self, ctx:Ah5Parser.For_statementContext):
        pass


    # Enter a parse tree produced by Ah5Parser#until_statement.
    def enterUntil_statement(self, ctx:Ah5Parser.Until_statementContext):
        pass

    # Exit a parse tree produced by Ah5Parser#until_statement.
    def exitUntil_statement(self, ctx:Ah5Parser.Until_statementContext):
        pass


    # Enter a parse tree produced by Ah5Parser#while_statement.
    def enterWhile_statement(self, ctx:Ah5Parser.While_statementContext):
        pass

    # Exit a parse tree produced by Ah5Parser#while_statement.
    def exitWhile_statement(self, ctx:Ah5Parser.While_statementContext):
        pass


    # Enter a parse tree produced by Ah5Parser#switch_statement.
    def enterSwitch_statement(self, ctx:Ah5Parser.Switch_statementContext):
        pass

    # Exit a parse tree produced by Ah5Parser#switch_statement.
    def exitSwitch_statement(self, ctx:Ah5Parser.Switch_statementContext):
        pass


    # Enter a parse tree produced by Ah5Parser#case_statement.
    def enterCase_statement(self, ctx:Ah5Parser.Case_statementContext):
        pass

    # Exit a parse tree produced by Ah5Parser#case_statement.
    def exitCase_statement(self, ctx:Ah5Parser.Case_statementContext):
        pass


    # Enter a parse tree produced by Ah5Parser#default_statement.
    def enterDefault_statement(self, ctx:Ah5Parser.Default_statementContext):
        pass

    # Exit a parse tree produced by Ah5Parser#default_statement.
    def exitDefault_statement(self, ctx:Ah5Parser.Default_statementContext):
        pass


    # Enter a parse tree produced by Ah5Parser#range_function.
    def enterRange_function(self, ctx:Ah5Parser.Range_functionContext):
        pass

    # Exit a parse tree produced by Ah5Parser#range_function.
    def exitRange_function(self, ctx:Ah5Parser.Range_functionContext):
        pass


    # Enter a parse tree produced by Ah5Parser#block.
    def enterBlock(self, ctx:Ah5Parser.BlockContext):
        pass

    # Exit a parse tree produced by Ah5Parser#block.
    def exitBlock(self, ctx:Ah5Parser.BlockContext):
        pass


    # Enter a parse tree produced by Ah5Parser#done_statement.
    def enterDone_statement(self, ctx:Ah5Parser.Done_statementContext):
        pass

    # Exit a parse tree produced by Ah5Parser#done_statement.
    def exitDone_statement(self, ctx:Ah5Parser.Done_statementContext):
        pass


    # Enter a parse tree produced by Ah5Parser#continue_statement.
    def enterContinue_statement(self, ctx:Ah5Parser.Continue_statementContext):
        pass

    # Exit a parse tree produced by Ah5Parser#continue_statement.
    def exitContinue_statement(self, ctx:Ah5Parser.Continue_statementContext):
        pass


    # Enter a parse tree produced by Ah5Parser#os_statement.
    def enterOs_statement(self, ctx:Ah5Parser.Os_statementContext):
        pass

    # Exit a parse tree produced by Ah5Parser#os_statement.
    def exitOs_statement(self, ctx:Ah5Parser.Os_statementContext):
        pass


    # Enter a parse tree produced by Ah5Parser#log_statement.
    def enterLog_statement(self, ctx:Ah5Parser.Log_statementContext):
        pass

    # Exit a parse tree produced by Ah5Parser#log_statement.
    def exitLog_statement(self, ctx:Ah5Parser.Log_statementContext):
        pass


    # Enter a parse tree produced by Ah5Parser#flexible_parameter_block.
    def enterFlexible_parameter_block(self, ctx:Ah5Parser.Flexible_parameter_blockContext):
        pass

    # Exit a parse tree produced by Ah5Parser#flexible_parameter_block.
    def exitFlexible_parameter_block(self, ctx:Ah5Parser.Flexible_parameter_blockContext):
        pass


    # Enter a parse tree produced by Ah5Parser#flexible_parameter.
    def enterFlexible_parameter(self, ctx:Ah5Parser.Flexible_parameterContext):
        pass

    # Exit a parse tree produced by Ah5Parser#flexible_parameter.
    def exitFlexible_parameter(self, ctx:Ah5Parser.Flexible_parameterContext):
        pass


    # Enter a parse tree produced by Ah5Parser#import_statement.
    def enterImport_statement(self, ctx:Ah5Parser.Import_statementContext):
        pass

    # Exit a parse tree produced by Ah5Parser#import_statement.
    def exitImport_statement(self, ctx:Ah5Parser.Import_statementContext):
        pass


    # Enter a parse tree produced by Ah5Parser#extends_statement.
    def enterExtends_statement(self, ctx:Ah5Parser.Extends_statementContext):
        pass

    # Exit a parse tree produced by Ah5Parser#extends_statement.
    def exitExtends_statement(self, ctx:Ah5Parser.Extends_statementContext):
        pass


    # Enter a parse tree produced by Ah5Parser#atom_create_instance.
    def enterAtom_create_instance(self, ctx:Ah5Parser.Atom_create_instanceContext):
        pass

    # Exit a parse tree produced by Ah5Parser#atom_create_instance.
    def exitAtom_create_instance(self, ctx:Ah5Parser.Atom_create_instanceContext):
        pass


    # Enter a parse tree produced by Ah5Parser#ahoptions_statement.
    def enterAhoptions_statement(self, ctx:Ah5Parser.Ahoptions_statementContext):
        pass

    # Exit a parse tree produced by Ah5Parser#ahoptions_statement.
    def exitAhoptions_statement(self, ctx:Ah5Parser.Ahoptions_statementContext):
        pass


    # Enter a parse tree produced by Ah5Parser#optional_parameters_block.
    def enterOptional_parameters_block(self, ctx:Ah5Parser.Optional_parameters_blockContext):
        pass

    # Exit a parse tree produced by Ah5Parser#optional_parameters_block.
    def exitOptional_parameters_block(self, ctx:Ah5Parser.Optional_parameters_blockContext):
        pass


    # Enter a parse tree produced by Ah5Parser#optional_parameter.
    def enterOptional_parameter(self, ctx:Ah5Parser.Optional_parameterContext):
        pass

    # Exit a parse tree produced by Ah5Parser#optional_parameter.
    def exitOptional_parameter(self, ctx:Ah5Parser.Optional_parameterContext):
        pass


    # Enter a parse tree produced by Ah5Parser#dict_signal.
    def enterDict_signal(self, ctx:Ah5Parser.Dict_signalContext):
        pass

    # Exit a parse tree produced by Ah5Parser#dict_signal.
    def exitDict_signal(self, ctx:Ah5Parser.Dict_signalContext):
        pass


    # Enter a parse tree produced by Ah5Parser#casting.
    def enterCasting(self, ctx:Ah5Parser.CastingContext):
        pass

    # Exit a parse tree produced by Ah5Parser#casting.
    def exitCasting(self, ctx:Ah5Parser.CastingContext):
        pass


    # Enter a parse tree produced by Ah5Parser#assignment_statement.
    def enterAssignment_statement(self, ctx:Ah5Parser.Assignment_statementContext):
        pass

    # Exit a parse tree produced by Ah5Parser#assignment_statement.
    def exitAssignment_statement(self, ctx:Ah5Parser.Assignment_statementContext):
        pass


    # Enter a parse tree produced by Ah5Parser#data_type.
    def enterData_type(self, ctx:Ah5Parser.Data_typeContext):
        pass

    # Exit a parse tree produced by Ah5Parser#data_type.
    def exitData_type(self, ctx:Ah5Parser.Data_typeContext):
        pass


    # Enter a parse tree produced by Ah5Parser#atom_obj_dict.
    def enterAtom_obj_dict(self, ctx:Ah5Parser.Atom_obj_dictContext):
        pass

    # Exit a parse tree produced by Ah5Parser#atom_obj_dict.
    def exitAtom_obj_dict(self, ctx:Ah5Parser.Atom_obj_dictContext):
        pass


    # Enter a parse tree produced by Ah5Parser#dict_comp.
    def enterDict_comp(self, ctx:Ah5Parser.Dict_compContext):
        pass

    # Exit a parse tree produced by Ah5Parser#dict_comp.
    def exitDict_comp(self, ctx:Ah5Parser.Dict_compContext):
        pass


    # Enter a parse tree produced by Ah5Parser#atom_obj_list.
    def enterAtom_obj_list(self, ctx:Ah5Parser.Atom_obj_listContext):
        pass

    # Exit a parse tree produced by Ah5Parser#atom_obj_list.
    def exitAtom_obj_list(self, ctx:Ah5Parser.Atom_obj_listContext):
        pass


    # Enter a parse tree produced by Ah5Parser#atom_obj_enum.
    def enterAtom_obj_enum(self, ctx:Ah5Parser.Atom_obj_enumContext):
        pass

    # Exit a parse tree produced by Ah5Parser#atom_obj_enum.
    def exitAtom_obj_enum(self, ctx:Ah5Parser.Atom_obj_enumContext):
        pass


    # Enter a parse tree produced by Ah5Parser#error_statement.
    def enterError_statement(self, ctx:Ah5Parser.Error_statementContext):
        pass

    # Exit a parse tree produced by Ah5Parser#error_statement.
    def exitError_statement(self, ctx:Ah5Parser.Error_statementContext):
        pass


    # Enter a parse tree produced by Ah5Parser#inject.
    def enterInject(self, ctx:Ah5Parser.InjectContext):
        pass

    # Exit a parse tree produced by Ah5Parser#inject.
    def exitInject(self, ctx:Ah5Parser.InjectContext):
        pass


    # Enter a parse tree produced by Ah5Parser#condition.
    def enterCondition(self, ctx:Ah5Parser.ConditionContext):
        pass

    # Exit a parse tree produced by Ah5Parser#condition.
    def exitCondition(self, ctx:Ah5Parser.ConditionContext):
        pass


    # Enter a parse tree produced by Ah5Parser#return_statement.
    def enterReturn_statement(self, ctx:Ah5Parser.Return_statementContext):
        pass

    # Exit a parse tree produced by Ah5Parser#return_statement.
    def exitReturn_statement(self, ctx:Ah5Parser.Return_statementContext):
        pass


    # Enter a parse tree produced by Ah5Parser#typing.
    def enterTyping(self, ctx:Ah5Parser.TypingContext):
        pass

    # Exit a parse tree produced by Ah5Parser#typing.
    def exitTyping(self, ctx:Ah5Parser.TypingContext):
        pass


    # Enter a parse tree produced by Ah5Parser#count.
    def enterCount(self, ctx:Ah5Parser.CountContext):
        pass

    # Exit a parse tree produced by Ah5Parser#count.
    def exitCount(self, ctx:Ah5Parser.CountContext):
        pass


    # Enter a parse tree produced by Ah5Parser#delete_statement.
    def enterDelete_statement(self, ctx:Ah5Parser.Delete_statementContext):
        pass

    # Exit a parse tree produced by Ah5Parser#delete_statement.
    def exitDelete_statement(self, ctx:Ah5Parser.Delete_statementContext):
        pass


    # Enter a parse tree produced by Ah5Parser#await_statement.
    def enterAwait_statement(self, ctx:Ah5Parser.Await_statementContext):
        pass

    # Exit a parse tree produced by Ah5Parser#await_statement.
    def exitAwait_statement(self, ctx:Ah5Parser.Await_statementContext):
        pass


    # Enter a parse tree produced by Ah5Parser#reflection.
    def enterReflection(self, ctx:Ah5Parser.ReflectionContext):
        pass

    # Exit a parse tree produced by Ah5Parser#reflection.
    def exitReflection(self, ctx:Ah5Parser.ReflectionContext):
        pass


    # Enter a parse tree produced by Ah5Parser#required_parameter.
    def enterRequired_parameter(self, ctx:Ah5Parser.Required_parameterContext):
        pass

    # Exit a parse tree produced by Ah5Parser#required_parameter.
    def exitRequired_parameter(self, ctx:Ah5Parser.Required_parameterContext):
        pass


    # Enter a parse tree produced by Ah5Parser#labels.
    def enterLabels(self, ctx:Ah5Parser.LabelsContext):
        pass

    # Exit a parse tree produced by Ah5Parser#labels.
    def exitLabels(self, ctx:Ah5Parser.LabelsContext):
        pass


    # Enter a parse tree produced by Ah5Parser#label_comp.
    def enterLabel_comp(self, ctx:Ah5Parser.Label_compContext):
        pass

    # Exit a parse tree produced by Ah5Parser#label_comp.
    def exitLabel_comp(self, ctx:Ah5Parser.Label_compContext):
        pass


    # Enter a parse tree produced by Ah5Parser#label.
    def enterLabel(self, ctx:Ah5Parser.LabelContext):
        pass

    # Exit a parse tree produced by Ah5Parser#label.
    def exitLabel(self, ctx:Ah5Parser.LabelContext):
        pass


    # Enter a parse tree produced by Ah5Parser#attributes.
    def enterAttributes(self, ctx:Ah5Parser.AttributesContext):
        pass

    # Exit a parse tree produced by Ah5Parser#attributes.
    def exitAttributes(self, ctx:Ah5Parser.AttributesContext):
        pass


    # Enter a parse tree produced by Ah5Parser#atom_string.
    def enterAtom_string(self, ctx:Ah5Parser.Atom_stringContext):
        pass

    # Exit a parse tree produced by Ah5Parser#atom_string.
    def exitAtom_string(self, ctx:Ah5Parser.Atom_stringContext):
        pass


    # Enter a parse tree produced by Ah5Parser#atom_number.
    def enterAtom_number(self, ctx:Ah5Parser.Atom_numberContext):
        pass

    # Exit a parse tree produced by Ah5Parser#atom_number.
    def exitAtom_number(self, ctx:Ah5Parser.Atom_numberContext):
        pass


    # Enter a parse tree produced by Ah5Parser#atom_boolean.
    def enterAtom_boolean(self, ctx:Ah5Parser.Atom_booleanContext):
        pass

    # Exit a parse tree produced by Ah5Parser#atom_boolean.
    def exitAtom_boolean(self, ctx:Ah5Parser.Atom_booleanContext):
        pass


    # Enter a parse tree produced by Ah5Parser#atom_hex.
    def enterAtom_hex(self, ctx:Ah5Parser.Atom_hexContext):
        pass

    # Exit a parse tree produced by Ah5Parser#atom_hex.
    def exitAtom_hex(self, ctx:Ah5Parser.Atom_hexContext):
        pass


    # Enter a parse tree produced by Ah5Parser#atom_none.
    def enterAtom_none(self, ctx:Ah5Parser.Atom_noneContext):
        pass

    # Exit a parse tree produced by Ah5Parser#atom_none.
    def exitAtom_none(self, ctx:Ah5Parser.Atom_noneContext):
        pass


