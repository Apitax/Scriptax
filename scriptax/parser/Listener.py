from antlr4 import *
from scriptax.grammar.build.Ah4Parser import Ah4Parser
from scriptax.grammar.build.Ah4Listener import Ah4Listener as AhListenerOriginal


class AhListener(AhListenerOriginal):
    def enterProg(self, ctx: Ah4Parser.ProgContext):
        super().enterProg(ctx)

    def exitProg(self, ctx: Ah4Parser.ProgContext):
        super().exitProg(ctx)

    def enterScript_structure(self, ctx: Ah4Parser.Script_structureContext):
        super().enterScript_structure(ctx)

    def exitScript_structure(self, ctx: Ah4Parser.Script_structureContext):
        super().exitScript_structure(ctx)

    def enterGlobal_statements(self, ctx: Ah4Parser.Global_statementsContext):
        super().enterGlobal_statements(ctx)

    def exitGlobal_statements(self, ctx: Ah4Parser.Global_statementsContext):
        super().exitGlobal_statements(ctx)

    def enterRoot_level_statements(self, ctx: Ah4Parser.Root_level_statementsContext):
        super().enterRoot_level_statements(ctx)

    def exitRoot_level_statements(self, ctx: Ah4Parser.Root_level_statementsContext):
        super().exitRoot_level_statements(ctx)

    def enterStatements(self, ctx: Ah4Parser.StatementsContext):
        super().enterStatements(ctx)

    def exitStatements(self, ctx: Ah4Parser.StatementsContext):
        super().exitStatements(ctx)

    def enterStatement(self, ctx: Ah4Parser.StatementContext):
        super().enterStatement(ctx)

    def exitStatement(self, ctx: Ah4Parser.StatementContext):
        super().exitStatement(ctx)

    def enterExpr(self, ctx: Ah4Parser.ExprContext):
        super().enterExpr(ctx)

    def exitExpr(self, ctx: Ah4Parser.ExprContext):
        super().exitExpr(ctx)

    def enterAtom(self, ctx: Ah4Parser.AtomContext):
        super().enterAtom(ctx)

    def exitAtom(self, ctx: Ah4Parser.AtomContext):
        super().exitAtom(ctx)

    def enterTerminated(self, ctx: Ah4Parser.TerminatedContext):
        super().enterTerminated(ctx)

    def exitTerminated(self, ctx: Ah4Parser.TerminatedContext):
        super().exitTerminated(ctx)

    def enterRunnable_statements(self, ctx: Ah4Parser.Runnable_statementsContext):
        super().enterRunnable_statements(ctx)

    def exitRunnable_statements(self, ctx: Ah4Parser.Runnable_statementsContext):
        super().exitRunnable_statements(ctx)

    def enterMethod_call_statement(self, ctx: Ah4Parser.Method_call_statementContext):
        super().enterMethod_call_statement(ctx)

    def exitMethod_call_statement(self, ctx: Ah4Parser.Method_call_statementContext):
        super().exitMethod_call_statement(ctx)

    def enterCommandtax_statement(self, ctx: Ah4Parser.Commandtax_statementContext):
        super().enterCommandtax_statement(ctx)

    def exitCommandtax_statement(self, ctx: Ah4Parser.Commandtax_statementContext):
        super().exitCommandtax_statement(ctx)

    def enterOs_statement(self, ctx: Ah4Parser.Os_statementContext):
        super().enterOs_statement(ctx)

    def exitOs_statement(self, ctx: Ah4Parser.Os_statementContext):
        super().exitOs_statement(ctx)

    def enterEach_statement(self, ctx: Ah4Parser.Each_statementContext):
        super().enterEach_statement(ctx)

    def exitEach_statement(self, ctx: Ah4Parser.Each_statementContext):
        super().exitEach_statement(ctx)

    def enterAtom_callback(self, ctx: Ah4Parser.Atom_callbackContext):
        super().enterAtom_callback(ctx)

    def exitAtom_callback(self, ctx: Ah4Parser.Atom_callbackContext):
        super().exitAtom_callback(ctx)

    def enterCallback_block(self, ctx: Ah4Parser.Callback_blockContext):
        super().enterCallback_block(ctx)

    def exitCallback_block(self, ctx: Ah4Parser.Callback_blockContext):
        super().exitCallback_block(ctx)

    def enterMethod_def_atom(self, ctx: Ah4Parser.Method_def_atomContext):
        super().enterMethod_def_atom(ctx)

    def exitMethod_def_atom(self, ctx: Ah4Parser.Method_def_atomContext):
        super().exitMethod_def_atom(ctx)

    def enterNon_terminated(self, ctx: Ah4Parser.Non_terminatedContext):
        super().enterNon_terminated(ctx)

    def exitNon_terminated(self, ctx: Ah4Parser.Non_terminatedContext):
        super().exitNon_terminated(ctx)

    def enterFlow(self, ctx: Ah4Parser.FlowContext):
        super().enterFlow(ctx)

    def exitFlow(self, ctx: Ah4Parser.FlowContext):
        super().exitFlow(ctx)

    def enterIf_statement(self, ctx: Ah4Parser.If_statementContext):
        super().enterIf_statement(ctx)

    def exitIf_statement(self, ctx: Ah4Parser.If_statementContext):
        super().exitIf_statement(ctx)

    def enterFor_statement(self, ctx: Ah4Parser.For_statementContext):
        super().enterFor_statement(ctx)

    def exitFor_statement(self, ctx: Ah4Parser.For_statementContext):
        super().exitFor_statement(ctx)

    def enterWhile_statement(self, ctx: Ah4Parser.While_statementContext):
        super().enterWhile_statement(ctx)

    def exitWhile_statement(self, ctx: Ah4Parser.While_statementContext):
        super().exitWhile_statement(ctx)

    def enterSwitch_statement(self, ctx: Ah4Parser.Switch_statementContext):
        super().enterSwitch_statement(ctx)

    def exitSwitch_statement(self, ctx: Ah4Parser.Switch_statementContext):
        super().exitSwitch_statement(ctx)

    def enterCase_statement(self, ctx: Ah4Parser.Case_statementContext):
        super().enterCase_statement(ctx)

    def exitCase_statement(self, ctx: Ah4Parser.Case_statementContext):
        super().exitCase_statement(ctx)

    def enterDefault_statement(self, ctx: Ah4Parser.Default_statementContext):
        super().enterDefault_statement(ctx)

    def exitDefault_statement(self, ctx: Ah4Parser.Default_statementContext):
        super().exitDefault_statement(ctx)

    def enterBlock(self, ctx: Ah4Parser.BlockContext):
        super().enterBlock(ctx)

    def exitBlock(self, ctx: Ah4Parser.BlockContext):
        super().exitBlock(ctx)

    def enterLog_statement(self, ctx: Ah4Parser.Log_statementContext):
        super().enterLog_statement(ctx)

    def exitLog_statement(self, ctx: Ah4Parser.Log_statementContext):
        super().exitLog_statement(ctx)

    def enterFlexible_parameter_block(self, ctx: Ah4Parser.Flexible_parameter_blockContext):
        super().enterFlexible_parameter_block(ctx)

    def exitFlexible_parameter_block(self, ctx: Ah4Parser.Flexible_parameter_blockContext):
        super().exitFlexible_parameter_block(ctx)

    def enterFlexible_parameter(self, ctx: Ah4Parser.Flexible_parameterContext):
        super().enterFlexible_parameter(ctx)

    def exitFlexible_parameter(self, ctx: Ah4Parser.Flexible_parameterContext):
        super().exitFlexible_parameter(ctx)

    def enterImport_statement(self, ctx: Ah4Parser.Import_statementContext):
        super().enterImport_statement(ctx)

    def exitImport_statement(self, ctx: Ah4Parser.Import_statementContext):
        super().exitImport_statement(ctx)

    def enterExtends_statement(self, ctx: Ah4Parser.Extends_statementContext):
        super().enterExtends_statement(ctx)

    def exitExtends_statement(self, ctx: Ah4Parser.Extends_statementContext):
        super().exitExtends_statement(ctx)

    def enterCreate_instance(self, ctx: Ah4Parser.Create_instanceContext):
        super().enterCreate_instance(ctx)

    def exitCreate_instance(self, ctx: Ah4Parser.Create_instanceContext):
        super().exitCreate_instance(ctx)

    def enterAhoptions_statement(self, ctx: Ah4Parser.Ahoptions_statementContext):
        super().enterAhoptions_statement(ctx)

    def exitAhoptions_statement(self, ctx: Ah4Parser.Ahoptions_statementContext):
        super().exitAhoptions_statement(ctx)

    def enterOptional_parameters_block(self, ctx: Ah4Parser.Optional_parameters_blockContext):
        super().enterOptional_parameters_block(ctx)

    def exitOptional_parameters_block(self, ctx: Ah4Parser.Optional_parameters_blockContext):
        super().exitOptional_parameters_block(ctx)

    def enterOptional_parameter(self, ctx: Ah4Parser.Optional_parameterContext):
        super().enterOptional_parameter(ctx)

    def exitOptional_parameter(self, ctx: Ah4Parser.Optional_parameterContext):
        super().exitOptional_parameter(ctx)

    def enterDict_signal(self, ctx: Ah4Parser.Dict_signalContext):
        super().enterDict_signal(ctx)

    def exitDict_signal(self, ctx: Ah4Parser.Dict_signalContext):
        super().exitDict_signal(ctx)

    def enterCasting(self, ctx: Ah4Parser.CastingContext):
        super().enterCasting(ctx)

    def exitCasting(self, ctx: Ah4Parser.CastingContext):
        super().exitCasting(ctx)

    def enterAtom_obj_dict(self, ctx: Ah4Parser.Atom_obj_dictContext):
        super().enterAtom_obj_dict(ctx)

    def exitAtom_obj_dict(self, ctx: Ah4Parser.Atom_obj_dictContext):
        super().exitAtom_obj_dict(ctx)

    def enterAssignment_statement(self, ctx: Ah4Parser.Assignment_statementContext):
        super().enterAssignment_statement(ctx)

    def exitAssignment_statement(self, ctx: Ah4Parser.Assignment_statementContext):
        super().exitAssignment_statement(ctx)

    def enterAtom_obj_list(self, ctx: Ah4Parser.Atom_obj_listContext):
        super().enterAtom_obj_list(ctx)

    def exitAtom_obj_list(self, ctx: Ah4Parser.Atom_obj_listContext):
        super().exitAtom_obj_list(ctx)

    def enterAtom_obj_enum(self, ctx: Ah4Parser.Atom_obj_enumContext):
        super().enterAtom_obj_enum(ctx)

    def exitAtom_obj_enum(self, ctx: Ah4Parser.Atom_obj_enumContext):
        super().exitAtom_obj_enum(ctx)

    def enterError_statement(self, ctx: Ah4Parser.Error_statementContext):
        super().enterError_statement(ctx)

    def exitError_statement(self, ctx: Ah4Parser.Error_statementContext):
        super().exitError_statement(ctx)

    def enterInject(self, ctx: Ah4Parser.InjectContext):
        super().enterInject(ctx)

    def exitInject(self, ctx: Ah4Parser.InjectContext):
        super().exitInject(ctx)

    def enterCondition(self, ctx: Ah4Parser.ConditionContext):
        super().enterCondition(ctx)

    def exitCondition(self, ctx: Ah4Parser.ConditionContext):
        super().exitCondition(ctx)

    def enterReturn_statement(self, ctx: Ah4Parser.Return_statementContext):
        super().enterReturn_statement(ctx)

    def exitReturn_statement(self, ctx: Ah4Parser.Return_statementContext):
        super().exitReturn_statement(ctx)

    def enterCount(self, ctx: Ah4Parser.CountContext):
        super().enterCount(ctx)

    def exitCount(self, ctx: Ah4Parser.CountContext):
        super().exitCount(ctx)

    def enterDelete_statement(self, ctx: Ah4Parser.Delete_statementContext):
        super().enterDelete_statement(ctx)

    def exitDelete_statement(self, ctx: Ah4Parser.Delete_statementContext):
        super().exitDelete_statement(ctx)

    def enterAwait_statement(self, ctx: Ah4Parser.Await_statementContext):
        super().enterAwait_statement(ctx)

    def exitAwait_statement(self, ctx: Ah4Parser.Await_statementContext):
        super().exitAwait_statement(ctx)

    def enterReflection(self, ctx: Ah4Parser.ReflectionContext):
        super().enterReflection(ctx)

    def exitReflection(self, ctx: Ah4Parser.ReflectionContext):
        super().exitReflection(ctx)

    def enterRequired_parameter(self, ctx: Ah4Parser.Required_parameterContext):
        super().enterRequired_parameter(ctx)

    def exitRequired_parameter(self, ctx: Ah4Parser.Required_parameterContext):
        super().exitRequired_parameter(ctx)

    def enterLabels(self, ctx: Ah4Parser.LabelsContext):
        super().enterLabels(ctx)

    def exitLabels(self, ctx: Ah4Parser.LabelsContext):
        super().exitLabels(ctx)

    def enterLabel_comp(self, ctx: Ah4Parser.Label_compContext):
        super().enterLabel_comp(ctx)

    def exitLabel_comp(self, ctx: Ah4Parser.Label_compContext):
        super().exitLabel_comp(ctx)

    def enterLabel(self, ctx: Ah4Parser.LabelContext):
        super().enterLabel(ctx)

    def exitLabel(self, ctx: Ah4Parser.LabelContext):
        super().exitLabel(ctx)

    def enterAttribute(self, ctx: Ah4Parser.AttributeContext):
        super().enterAttribute(ctx)

    def exitAttribute(self, ctx: Ah4Parser.AttributeContext):
        super().exitAttribute(ctx)

    def enterAtom_string(self, ctx: Ah4Parser.Atom_stringContext):
        super().enterAtom_string(ctx)

    def exitAtom_string(self, ctx: Ah4Parser.Atom_stringContext):
        super().exitAtom_string(ctx)

    def enterAtom_number(self, ctx: Ah4Parser.Atom_numberContext):
        super().enterAtom_number(ctx)

    def exitAtom_number(self, ctx: Ah4Parser.Atom_numberContext):
        super().exitAtom_number(ctx)

    def enterAtom_boolean(self, ctx: Ah4Parser.Atom_booleanContext):
        super().enterAtom_boolean(ctx)

    def exitAtom_boolean(self, ctx: Ah4Parser.Atom_booleanContext):
        super().exitAtom_boolean(ctx)

    def enterAtom_hex(self, ctx: Ah4Parser.Atom_hexContext):
        super().enterAtom_hex(ctx)

    def exitAtom_hex(self, ctx: Ah4Parser.Atom_hexContext):
        super().exitAtom_hex(ctx)

    def enterAtom_none(self, ctx: Ah4Parser.Atom_noneContext):
        super().enterAtom_none(ctx)

    def exitAtom_none(self, ctx: Ah4Parser.Atom_noneContext):
        super().exitAtom_none(ctx)