# Generated from src/Ah4.g4 by ANTLR 4.7.2
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .Ah4Parser import Ah4Parser
else:
    from Ah4Parser import Ah4Parser

# This class defines a complete listener for a parse tree produced by Ah4Parser.
class Ah4Listener(ParseTreeListener):

    # Enter a parse tree produced by Ah4Parser#prog.
    def enterProg(self, ctx:Ah4Parser.ProgContext):
        pass

    # Exit a parse tree produced by Ah4Parser#prog.
    def exitProg(self, ctx:Ah4Parser.ProgContext):
        pass


    # Enter a parse tree produced by Ah4Parser#script_structure.
    def enterScript_structure(self, ctx:Ah4Parser.Script_structureContext):
        pass

    # Exit a parse tree produced by Ah4Parser#script_structure.
    def exitScript_structure(self, ctx:Ah4Parser.Script_structureContext):
        pass


    # Enter a parse tree produced by Ah4Parser#global_statements.
    def enterGlobal_statements(self, ctx:Ah4Parser.Global_statementsContext):
        pass

    # Exit a parse tree produced by Ah4Parser#global_statements.
    def exitGlobal_statements(self, ctx:Ah4Parser.Global_statementsContext):
        pass


    # Enter a parse tree produced by Ah4Parser#root_level_statements.
    def enterRoot_level_statements(self, ctx:Ah4Parser.Root_level_statementsContext):
        pass

    # Exit a parse tree produced by Ah4Parser#root_level_statements.
    def exitRoot_level_statements(self, ctx:Ah4Parser.Root_level_statementsContext):
        pass


    # Enter a parse tree produced by Ah4Parser#statements.
    def enterStatements(self, ctx:Ah4Parser.StatementsContext):
        pass

    # Exit a parse tree produced by Ah4Parser#statements.
    def exitStatements(self, ctx:Ah4Parser.StatementsContext):
        pass


    # Enter a parse tree produced by Ah4Parser#statement.
    def enterStatement(self, ctx:Ah4Parser.StatementContext):
        pass

    # Exit a parse tree produced by Ah4Parser#statement.
    def exitStatement(self, ctx:Ah4Parser.StatementContext):
        pass


    # Enter a parse tree produced by Ah4Parser#expr.
    def enterExpr(self, ctx:Ah4Parser.ExprContext):
        pass

    # Exit a parse tree produced by Ah4Parser#expr.
    def exitExpr(self, ctx:Ah4Parser.ExprContext):
        pass


    # Enter a parse tree produced by Ah4Parser#atom.
    def enterAtom(self, ctx:Ah4Parser.AtomContext):
        pass

    # Exit a parse tree produced by Ah4Parser#atom.
    def exitAtom(self, ctx:Ah4Parser.AtomContext):
        pass


    # Enter a parse tree produced by Ah4Parser#terminated.
    def enterTerminated(self, ctx:Ah4Parser.TerminatedContext):
        pass

    # Exit a parse tree produced by Ah4Parser#terminated.
    def exitTerminated(self, ctx:Ah4Parser.TerminatedContext):
        pass


    # Enter a parse tree produced by Ah4Parser#runnable_statements.
    def enterRunnable_statements(self, ctx:Ah4Parser.Runnable_statementsContext):
        pass

    # Exit a parse tree produced by Ah4Parser#runnable_statements.
    def exitRunnable_statements(self, ctx:Ah4Parser.Runnable_statementsContext):
        pass


    # Enter a parse tree produced by Ah4Parser#method_call_statement.
    def enterMethod_call_statement(self, ctx:Ah4Parser.Method_call_statementContext):
        pass

    # Exit a parse tree produced by Ah4Parser#method_call_statement.
    def exitMethod_call_statement(self, ctx:Ah4Parser.Method_call_statementContext):
        pass


    # Enter a parse tree produced by Ah4Parser#commandtax_statement.
    def enterCommandtax_statement(self, ctx:Ah4Parser.Commandtax_statementContext):
        pass

    # Exit a parse tree produced by Ah4Parser#commandtax_statement.
    def exitCommandtax_statement(self, ctx:Ah4Parser.Commandtax_statementContext):
        pass


    # Enter a parse tree produced by Ah4Parser#os_statement.
    def enterOs_statement(self, ctx:Ah4Parser.Os_statementContext):
        pass

    # Exit a parse tree produced by Ah4Parser#os_statement.
    def exitOs_statement(self, ctx:Ah4Parser.Os_statementContext):
        pass


    # Enter a parse tree produced by Ah4Parser#each_statement.
    def enterEach_statement(self, ctx:Ah4Parser.Each_statementContext):
        pass

    # Exit a parse tree produced by Ah4Parser#each_statement.
    def exitEach_statement(self, ctx:Ah4Parser.Each_statementContext):
        pass


    # Enter a parse tree produced by Ah4Parser#atom_callback.
    def enterAtom_callback(self, ctx:Ah4Parser.Atom_callbackContext):
        pass

    # Exit a parse tree produced by Ah4Parser#atom_callback.
    def exitAtom_callback(self, ctx:Ah4Parser.Atom_callbackContext):
        pass


    # Enter a parse tree produced by Ah4Parser#callback_block.
    def enterCallback_block(self, ctx:Ah4Parser.Callback_blockContext):
        pass

    # Exit a parse tree produced by Ah4Parser#callback_block.
    def exitCallback_block(self, ctx:Ah4Parser.Callback_blockContext):
        pass


    # Enter a parse tree produced by Ah4Parser#method_def_atom.
    def enterMethod_def_atom(self, ctx:Ah4Parser.Method_def_atomContext):
        pass

    # Exit a parse tree produced by Ah4Parser#method_def_atom.
    def exitMethod_def_atom(self, ctx:Ah4Parser.Method_def_atomContext):
        pass


    # Enter a parse tree produced by Ah4Parser#non_terminated.
    def enterNon_terminated(self, ctx:Ah4Parser.Non_terminatedContext):
        pass

    # Exit a parse tree produced by Ah4Parser#non_terminated.
    def exitNon_terminated(self, ctx:Ah4Parser.Non_terminatedContext):
        pass


    # Enter a parse tree produced by Ah4Parser#flow.
    def enterFlow(self, ctx:Ah4Parser.FlowContext):
        pass

    # Exit a parse tree produced by Ah4Parser#flow.
    def exitFlow(self, ctx:Ah4Parser.FlowContext):
        pass


    # Enter a parse tree produced by Ah4Parser#if_statement.
    def enterIf_statement(self, ctx:Ah4Parser.If_statementContext):
        pass

    # Exit a parse tree produced by Ah4Parser#if_statement.
    def exitIf_statement(self, ctx:Ah4Parser.If_statementContext):
        pass


    # Enter a parse tree produced by Ah4Parser#for_statement.
    def enterFor_statement(self, ctx:Ah4Parser.For_statementContext):
        pass

    # Exit a parse tree produced by Ah4Parser#for_statement.
    def exitFor_statement(self, ctx:Ah4Parser.For_statementContext):
        pass


    # Enter a parse tree produced by Ah4Parser#while_statement.
    def enterWhile_statement(self, ctx:Ah4Parser.While_statementContext):
        pass

    # Exit a parse tree produced by Ah4Parser#while_statement.
    def exitWhile_statement(self, ctx:Ah4Parser.While_statementContext):
        pass


    # Enter a parse tree produced by Ah4Parser#switch_statement.
    def enterSwitch_statement(self, ctx:Ah4Parser.Switch_statementContext):
        pass

    # Exit a parse tree produced by Ah4Parser#switch_statement.
    def exitSwitch_statement(self, ctx:Ah4Parser.Switch_statementContext):
        pass


    # Enter a parse tree produced by Ah4Parser#case_statement.
    def enterCase_statement(self, ctx:Ah4Parser.Case_statementContext):
        pass

    # Exit a parse tree produced by Ah4Parser#case_statement.
    def exitCase_statement(self, ctx:Ah4Parser.Case_statementContext):
        pass


    # Enter a parse tree produced by Ah4Parser#default_statement.
    def enterDefault_statement(self, ctx:Ah4Parser.Default_statementContext):
        pass

    # Exit a parse tree produced by Ah4Parser#default_statement.
    def exitDefault_statement(self, ctx:Ah4Parser.Default_statementContext):
        pass


    # Enter a parse tree produced by Ah4Parser#block.
    def enterBlock(self, ctx:Ah4Parser.BlockContext):
        pass

    # Exit a parse tree produced by Ah4Parser#block.
    def exitBlock(self, ctx:Ah4Parser.BlockContext):
        pass


    # Enter a parse tree produced by Ah4Parser#done_statement.
    def enterDone_statement(self, ctx:Ah4Parser.Done_statementContext):
        pass

    # Exit a parse tree produced by Ah4Parser#done_statement.
    def exitDone_statement(self, ctx:Ah4Parser.Done_statementContext):
        pass


    # Enter a parse tree produced by Ah4Parser#continue_statement.
    def enterContinue_statement(self, ctx:Ah4Parser.Continue_statementContext):
        pass

    # Exit a parse tree produced by Ah4Parser#continue_statement.
    def exitContinue_statement(self, ctx:Ah4Parser.Continue_statementContext):
        pass


    # Enter a parse tree produced by Ah4Parser#log_statement.
    def enterLog_statement(self, ctx:Ah4Parser.Log_statementContext):
        pass

    # Exit a parse tree produced by Ah4Parser#log_statement.
    def exitLog_statement(self, ctx:Ah4Parser.Log_statementContext):
        pass


    # Enter a parse tree produced by Ah4Parser#flexible_parameter_block.
    def enterFlexible_parameter_block(self, ctx:Ah4Parser.Flexible_parameter_blockContext):
        pass

    # Exit a parse tree produced by Ah4Parser#flexible_parameter_block.
    def exitFlexible_parameter_block(self, ctx:Ah4Parser.Flexible_parameter_blockContext):
        pass


    # Enter a parse tree produced by Ah4Parser#flexible_parameter.
    def enterFlexible_parameter(self, ctx:Ah4Parser.Flexible_parameterContext):
        pass

    # Exit a parse tree produced by Ah4Parser#flexible_parameter.
    def exitFlexible_parameter(self, ctx:Ah4Parser.Flexible_parameterContext):
        pass


    # Enter a parse tree produced by Ah4Parser#import_statement.
    def enterImport_statement(self, ctx:Ah4Parser.Import_statementContext):
        pass

    # Exit a parse tree produced by Ah4Parser#import_statement.
    def exitImport_statement(self, ctx:Ah4Parser.Import_statementContext):
        pass


    # Enter a parse tree produced by Ah4Parser#extends_statement.
    def enterExtends_statement(self, ctx:Ah4Parser.Extends_statementContext):
        pass

    # Exit a parse tree produced by Ah4Parser#extends_statement.
    def exitExtends_statement(self, ctx:Ah4Parser.Extends_statementContext):
        pass


    # Enter a parse tree produced by Ah4Parser#create_instance.
    def enterCreate_instance(self, ctx:Ah4Parser.Create_instanceContext):
        pass

    # Exit a parse tree produced by Ah4Parser#create_instance.
    def exitCreate_instance(self, ctx:Ah4Parser.Create_instanceContext):
        pass


    # Enter a parse tree produced by Ah4Parser#ahoptions_statement.
    def enterAhoptions_statement(self, ctx:Ah4Parser.Ahoptions_statementContext):
        pass

    # Exit a parse tree produced by Ah4Parser#ahoptions_statement.
    def exitAhoptions_statement(self, ctx:Ah4Parser.Ahoptions_statementContext):
        pass


    # Enter a parse tree produced by Ah4Parser#optional_parameters_block.
    def enterOptional_parameters_block(self, ctx:Ah4Parser.Optional_parameters_blockContext):
        pass

    # Exit a parse tree produced by Ah4Parser#optional_parameters_block.
    def exitOptional_parameters_block(self, ctx:Ah4Parser.Optional_parameters_blockContext):
        pass


    # Enter a parse tree produced by Ah4Parser#optional_parameter.
    def enterOptional_parameter(self, ctx:Ah4Parser.Optional_parameterContext):
        pass

    # Exit a parse tree produced by Ah4Parser#optional_parameter.
    def exitOptional_parameter(self, ctx:Ah4Parser.Optional_parameterContext):
        pass


    # Enter a parse tree produced by Ah4Parser#dict_signal.
    def enterDict_signal(self, ctx:Ah4Parser.Dict_signalContext):
        pass

    # Exit a parse tree produced by Ah4Parser#dict_signal.
    def exitDict_signal(self, ctx:Ah4Parser.Dict_signalContext):
        pass


    # Enter a parse tree produced by Ah4Parser#casting.
    def enterCasting(self, ctx:Ah4Parser.CastingContext):
        pass

    # Exit a parse tree produced by Ah4Parser#casting.
    def exitCasting(self, ctx:Ah4Parser.CastingContext):
        pass


    # Enter a parse tree produced by Ah4Parser#atom_obj_dict.
    def enterAtom_obj_dict(self, ctx:Ah4Parser.Atom_obj_dictContext):
        pass

    # Exit a parse tree produced by Ah4Parser#atom_obj_dict.
    def exitAtom_obj_dict(self, ctx:Ah4Parser.Atom_obj_dictContext):
        pass


    # Enter a parse tree produced by Ah4Parser#assignment_statement.
    def enterAssignment_statement(self, ctx:Ah4Parser.Assignment_statementContext):
        pass

    # Exit a parse tree produced by Ah4Parser#assignment_statement.
    def exitAssignment_statement(self, ctx:Ah4Parser.Assignment_statementContext):
        pass


    # Enter a parse tree produced by Ah4Parser#atom_obj_list.
    def enterAtom_obj_list(self, ctx:Ah4Parser.Atom_obj_listContext):
        pass

    # Exit a parse tree produced by Ah4Parser#atom_obj_list.
    def exitAtom_obj_list(self, ctx:Ah4Parser.Atom_obj_listContext):
        pass


    # Enter a parse tree produced by Ah4Parser#atom_obj_enum.
    def enterAtom_obj_enum(self, ctx:Ah4Parser.Atom_obj_enumContext):
        pass

    # Exit a parse tree produced by Ah4Parser#atom_obj_enum.
    def exitAtom_obj_enum(self, ctx:Ah4Parser.Atom_obj_enumContext):
        pass


    # Enter a parse tree produced by Ah4Parser#error_statement.
    def enterError_statement(self, ctx:Ah4Parser.Error_statementContext):
        pass

    # Exit a parse tree produced by Ah4Parser#error_statement.
    def exitError_statement(self, ctx:Ah4Parser.Error_statementContext):
        pass


    # Enter a parse tree produced by Ah4Parser#inject.
    def enterInject(self, ctx:Ah4Parser.InjectContext):
        pass

    # Exit a parse tree produced by Ah4Parser#inject.
    def exitInject(self, ctx:Ah4Parser.InjectContext):
        pass


    # Enter a parse tree produced by Ah4Parser#condition.
    def enterCondition(self, ctx:Ah4Parser.ConditionContext):
        pass

    # Exit a parse tree produced by Ah4Parser#condition.
    def exitCondition(self, ctx:Ah4Parser.ConditionContext):
        pass


    # Enter a parse tree produced by Ah4Parser#return_statement.
    def enterReturn_statement(self, ctx:Ah4Parser.Return_statementContext):
        pass

    # Exit a parse tree produced by Ah4Parser#return_statement.
    def exitReturn_statement(self, ctx:Ah4Parser.Return_statementContext):
        pass


    # Enter a parse tree produced by Ah4Parser#count.
    def enterCount(self, ctx:Ah4Parser.CountContext):
        pass

    # Exit a parse tree produced by Ah4Parser#count.
    def exitCount(self, ctx:Ah4Parser.CountContext):
        pass


    # Enter a parse tree produced by Ah4Parser#delete_statement.
    def enterDelete_statement(self, ctx:Ah4Parser.Delete_statementContext):
        pass

    # Exit a parse tree produced by Ah4Parser#delete_statement.
    def exitDelete_statement(self, ctx:Ah4Parser.Delete_statementContext):
        pass


    # Enter a parse tree produced by Ah4Parser#await_statement.
    def enterAwait_statement(self, ctx:Ah4Parser.Await_statementContext):
        pass

    # Exit a parse tree produced by Ah4Parser#await_statement.
    def exitAwait_statement(self, ctx:Ah4Parser.Await_statementContext):
        pass


    # Enter a parse tree produced by Ah4Parser#reflection.
    def enterReflection(self, ctx:Ah4Parser.ReflectionContext):
        pass

    # Exit a parse tree produced by Ah4Parser#reflection.
    def exitReflection(self, ctx:Ah4Parser.ReflectionContext):
        pass


    # Enter a parse tree produced by Ah4Parser#required_parameter.
    def enterRequired_parameter(self, ctx:Ah4Parser.Required_parameterContext):
        pass

    # Exit a parse tree produced by Ah4Parser#required_parameter.
    def exitRequired_parameter(self, ctx:Ah4Parser.Required_parameterContext):
        pass


    # Enter a parse tree produced by Ah4Parser#labels.
    def enterLabels(self, ctx:Ah4Parser.LabelsContext):
        pass

    # Exit a parse tree produced by Ah4Parser#labels.
    def exitLabels(self, ctx:Ah4Parser.LabelsContext):
        pass


    # Enter a parse tree produced by Ah4Parser#label_comp.
    def enterLabel_comp(self, ctx:Ah4Parser.Label_compContext):
        pass

    # Exit a parse tree produced by Ah4Parser#label_comp.
    def exitLabel_comp(self, ctx:Ah4Parser.Label_compContext):
        pass


    # Enter a parse tree produced by Ah4Parser#label.
    def enterLabel(self, ctx:Ah4Parser.LabelContext):
        pass

    # Exit a parse tree produced by Ah4Parser#label.
    def exitLabel(self, ctx:Ah4Parser.LabelContext):
        pass


    # Enter a parse tree produced by Ah4Parser#attributes.
    def enterAttributes(self, ctx:Ah4Parser.AttributesContext):
        pass

    # Exit a parse tree produced by Ah4Parser#attributes.
    def exitAttributes(self, ctx:Ah4Parser.AttributesContext):
        pass


    # Enter a parse tree produced by Ah4Parser#atom_string.
    def enterAtom_string(self, ctx:Ah4Parser.Atom_stringContext):
        pass

    # Exit a parse tree produced by Ah4Parser#atom_string.
    def exitAtom_string(self, ctx:Ah4Parser.Atom_stringContext):
        pass


    # Enter a parse tree produced by Ah4Parser#atom_number.
    def enterAtom_number(self, ctx:Ah4Parser.Atom_numberContext):
        pass

    # Exit a parse tree produced by Ah4Parser#atom_number.
    def exitAtom_number(self, ctx:Ah4Parser.Atom_numberContext):
        pass


    # Enter a parse tree produced by Ah4Parser#atom_boolean.
    def enterAtom_boolean(self, ctx:Ah4Parser.Atom_booleanContext):
        pass

    # Exit a parse tree produced by Ah4Parser#atom_boolean.
    def exitAtom_boolean(self, ctx:Ah4Parser.Atom_booleanContext):
        pass


    # Enter a parse tree produced by Ah4Parser#atom_hex.
    def enterAtom_hex(self, ctx:Ah4Parser.Atom_hexContext):
        pass

    # Exit a parse tree produced by Ah4Parser#atom_hex.
    def exitAtom_hex(self, ctx:Ah4Parser.Atom_hexContext):
        pass


    # Enter a parse tree produced by Ah4Parser#atom_none.
    def enterAtom_none(self, ctx:Ah4Parser.Atom_noneContext):
        pass

    # Exit a parse tree produced by Ah4Parser#atom_none.
    def exitAtom_none(self, ctx:Ah4Parser.Atom_noneContext):
        pass


