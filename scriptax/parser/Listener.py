from antlr4 import *
from scriptax.grammar.build.Ah3Parser import Ah3Parser
from scriptax.grammar.build.Ah3Listener import Ah3Listener as AhListenerOriginal


class AhListener(AhListenerOriginal):
    def enterProg(self, ctx: Ah3Parser.ProgContext):
        super().enterProg(ctx)

    def exitProg(self, ctx: Ah3Parser.ProgContext):
        super().exitProg(ctx)

    def enterScript_structure(self, ctx: Ah3Parser.Script_structureContext):
        super().enterScript_structure(ctx)

    def exitScript_structure(self, ctx: Ah3Parser.Script_structureContext):
        super().exitScript_structure(ctx)

    def enterGlobal_statements(self, ctx: Ah3Parser.Global_statementsContext):
        super().enterGlobal_statements(ctx)

    def exitGlobal_statements(self, ctx: Ah3Parser.Global_statementsContext):
        super().exitGlobal_statements(ctx)

    def enterStatements(self, ctx: Ah3Parser.StatementsContext):
        super().enterStatements(ctx)

    def exitStatements(self, ctx: Ah3Parser.StatementsContext):
        super().exitStatements(ctx)

    def enterStatement(self, ctx: Ah3Parser.StatementContext):
        super().enterStatement(ctx)

    def exitStatement(self, ctx: Ah3Parser.StatementContext):
        super().exitStatement(ctx)

    def enterTerminated(self, ctx: Ah3Parser.TerminatedContext):
        super().enterTerminated(ctx)

    def exitTerminated(self, ctx: Ah3Parser.TerminatedContext):
        super().exitTerminated(ctx)

    def enterNon_terminated(self, ctx: Ah3Parser.Non_terminatedContext):
        super().enterNon_terminated(ctx)

    def exitNon_terminated(self, ctx: Ah3Parser.Non_terminatedContext):
        super().exitNon_terminated(ctx)

    def enterExecute_statement(self, ctx: Ah3Parser.Execute_statementContext):
        super().enterExecute_statement(ctx)

    def exitExecute_statement(self, ctx: Ah3Parser.Execute_statementContext):
        super().exitExecute_statement(ctx)

    def enterExpr(self, ctx: Ah3Parser.ExprContext):
        super().enterExpr(ctx)

    def exitExpr(self, ctx: Ah3Parser.ExprContext):
        super().exitExpr(ctx)

    def enterAssignment(self, ctx: Ah3Parser.AssignmentContext):
        super().enterAssignment(ctx)

    def exitAssignment(self, ctx: Ah3Parser.AssignmentContext):
        super().exitAssignment(ctx)

    def enterFlow(self, ctx: Ah3Parser.FlowContext):
        super().enterFlow(ctx)

    def exitFlow(self, ctx: Ah3Parser.FlowContext):
        super().exitFlow(ctx)

    def enterCreate_instance(self, ctx: Ah3Parser.Create_instanceContext):
        super().enterCreate_instance(ctx)

    def exitCreate_instance(self, ctx: Ah3Parser.Create_instanceContext):
        super().exitCreate_instance(ctx)

    def enterMethod_statement(self, ctx: Ah3Parser.Method_statementContext):
        super().enterMethod_statement(ctx)

    def exitMethod_statement(self, ctx: Ah3Parser.Method_statementContext):
        super().exitMethod_statement(ctx)

    def enterMethod_call(self, ctx: Ah3Parser.Method_callContext):
        super().enterMethod_call(ctx)

    def exitMethod_call(self, ctx: Ah3Parser.Method_callContext):
        super().exitMethod_call(ctx)

    def enterIf_statement(self, ctx: Ah3Parser.If_statementContext):
        super().enterIf_statement(ctx)

    def exitIf_statement(self, ctx: Ah3Parser.If_statementContext):
        super().exitIf_statement(ctx)

    def enterWhile_statement(self, ctx: Ah3Parser.While_statementContext):
        super().enterWhile_statement(ctx)

    def exitWhile_statement(self, ctx: Ah3Parser.While_statementContext):
        super().exitWhile_statement(ctx)

    def enterFor_statement(self, ctx: Ah3Parser.For_statementContext):
        super().enterFor_statement(ctx)

    def exitFor_statement(self, ctx: Ah3Parser.For_statementContext):
        super().exitFor_statement(ctx)

    def enterEach_statement(self, ctx: Ah3Parser.Each_statementContext):
        super().enterEach_statement(ctx)

    def exitEach_statement(self, ctx: Ah3Parser.Each_statementContext):
        super().exitEach_statement(ctx)

    def enterCondition(self, ctx: Ah3Parser.ConditionContext):
        super().enterCondition(ctx)

    def exitCondition(self, ctx: Ah3Parser.ConditionContext):
        super().exitCondition(ctx)

    def enterBlock(self, ctx: Ah3Parser.BlockContext):
        super().enterBlock(ctx)

    def exitBlock(self, ctx: Ah3Parser.BlockContext):
        super().exitBlock(ctx)

    def enterCallback(self, ctx: Ah3Parser.CallbackContext):
        super().enterCallback(ctx)

    def exitCallback(self, ctx: Ah3Parser.CallbackContext):
        super().exitCallback(ctx)

    def enterCallback_block(self, ctx: Ah3Parser.Callback_blockContext):
        super().enterCallback_block(ctx)

    def exitCallback_block(self, ctx: Ah3Parser.Callback_blockContext):
        super().exitCallback_block(ctx)

    def enterOptional_parameters_block(self, ctx: Ah3Parser.Optional_parameters_blockContext):
        super().enterOptional_parameters_block(ctx)

    def exitOptional_parameters_block(self, ctx: Ah3Parser.Optional_parameters_blockContext):
        super().exitOptional_parameters_block(ctx)

    def enterSig_parameter_block(self, ctx: Ah3Parser.Sig_parameter_blockContext):
        super().enterSig_parameter_block(ctx)

    def exitSig_parameter_block(self, ctx: Ah3Parser.Sig_parameter_blockContext):
        super().exitSig_parameter_block(ctx)

    def enterSig_parameter(self, ctx: Ah3Parser.Sig_parameterContext):
        super().enterSig_parameter(ctx)

    def exitSig_parameter(self, ctx: Ah3Parser.Sig_parameterContext):
        super().exitSig_parameter(ctx)

    def enterCall_parameter(self, ctx: Ah3Parser.Call_parameterContext):
        super().enterCall_parameter(ctx)

    def exitCall_parameter(self, ctx: Ah3Parser.Call_parameterContext):
        super().exitCall_parameter(ctx)

    def enterOptional_parameter(self, ctx: Ah3Parser.Optional_parameterContext):
        super().enterOptional_parameter(ctx)

    def exitOptional_parameter(self, ctx: Ah3Parser.Optional_parameterContext):
        super().exitOptional_parameter(ctx)

    def enterCommandtax(self, ctx: Ah3Parser.CommandtaxContext):
        super().enterCommandtax(ctx)

    def exitCommandtax(self, ctx: Ah3Parser.CommandtaxContext):
        super().exitCommandtax(ctx)

    def enterExecute(self, ctx: Ah3Parser.ExecuteContext):
        super().enterExecute(ctx)

    def exitExecute(self, ctx: Ah3Parser.ExecuteContext):
        super().exitExecute(ctx)

    def enterAsync_execute(self, ctx: Ah3Parser.Async_executeContext):
        super().enterAsync_execute(ctx)

    def exitAsync_execute(self, ctx: Ah3Parser.Async_executeContext):
        super().exitAsync_execute(ctx)

    def enterAwait(self, ctx: Ah3Parser.AwaitContext):
        super().enterAwait(ctx)

    def exitAwait(self, ctx: Ah3Parser.AwaitContext):
        super().exitAwait(ctx)

    def enterLabels(self, ctx: Ah3Parser.LabelsContext):
        super().enterLabels(ctx)

    def exitLabels(self, ctx: Ah3Parser.LabelsContext):
        super().exitLabels(ctx)

    def enterLabel_comp(self, ctx: Ah3Parser.Label_compContext):
        super().enterLabel_comp(ctx)

    def exitLabel_comp(self, ctx: Ah3Parser.Label_compContext):
        super().exitLabel_comp(ctx)

    def enterLabel(self, ctx: Ah3Parser.LabelContext):
        super().enterLabel(ctx)

    def exitLabel(self, ctx: Ah3Parser.LabelContext):
        super().exitLabel(ctx)

    def enterAttribute(self, ctx: Ah3Parser.AttributeContext):
        super().enterAttribute(ctx)

    def exitAttribute(self, ctx: Ah3Parser.AttributeContext):
        super().exitAttribute(ctx)

    def enterExtends_statement(self, ctx: Ah3Parser.Extends_statementContext):
        super().enterExtends_statement(ctx)

    def exitExtends_statement(self, ctx: Ah3Parser.Extends_statementContext):
        super().exitExtends_statement(ctx)

    def enterSig_statement(self, ctx: Ah3Parser.Sig_statementContext):
        super().enterSig_statement(ctx)

    def exitSig_statement(self, ctx: Ah3Parser.Sig_statementContext):
        super().exitSig_statement(ctx)

    def enterOptions_statement(self, ctx: Ah3Parser.Options_statementContext):
        super().enterOptions_statement(ctx)

    def exitOptions_statement(self, ctx: Ah3Parser.Options_statementContext):
        super().exitOptions_statement(ctx)

    def enterDelete_statement(self, ctx: Ah3Parser.Delete_statementContext):
        super().enterDelete_statement(ctx)

    def exitDelete_statement(self, ctx: Ah3Parser.Delete_statementContext):
        super().exitDelete_statement(ctx)

    def enterError_statement(self, ctx: Ah3Parser.Error_statementContext):
        super().enterError_statement(ctx)

    def exitError_statement(self, ctx: Ah3Parser.Error_statementContext):
        super().exitError_statement(ctx)

    def enterReturn_statement(self, ctx: Ah3Parser.Return_statementContext):
        super().enterReturn_statement(ctx)

    def exitReturn_statement(self, ctx: Ah3Parser.Return_statementContext):
        super().exitReturn_statement(ctx)

    def enterLogin_statement(self, ctx: Ah3Parser.Login_statementContext):
        super().enterLogin_statement(ctx)

    def exitLogin_statement(self, ctx: Ah3Parser.Login_statementContext):
        super().exitLogin_statement(ctx)

    def enterEndpoint_statement(self, ctx: Ah3Parser.Endpoint_statementContext):
        super().enterEndpoint_statement(ctx)

    def exitEndpoint_statement(self, ctx: Ah3Parser.Endpoint_statementContext):
        super().exitEndpoint_statement(ctx)

    def enterImport_statement(self, ctx: Ah3Parser.Import_statementContext):
        super().enterImport_statement(ctx)

    def exitImport_statement(self, ctx: Ah3Parser.Import_statementContext):
        super().exitImport_statement(ctx)

    def enterCasting(self, ctx: Ah3Parser.CastingContext):
        super().enterCasting(ctx)

    def exitCasting(self, ctx: Ah3Parser.CastingContext):
        super().exitCasting(ctx)

    def enterAuth(self, ctx: Ah3Parser.AuthContext):
        super().enterAuth(ctx)

    def exitAuth(self, ctx: Ah3Parser.AuthContext):
        super().exitAuth(ctx)

    def enterUrl(self, ctx: Ah3Parser.UrlContext):
        super().enterUrl(ctx)

    def exitUrl(self, ctx: Ah3Parser.UrlContext):
        super().exitUrl(ctx)

    def enterLog(self, ctx: Ah3Parser.LogContext):
        super().enterLog(ctx)

    def exitLog(self, ctx: Ah3Parser.LogContext):
        super().exitLog(ctx)

    def enterCount(self, ctx: Ah3Parser.CountContext):
        super().enterCount(ctx)

    def exitCount(self, ctx: Ah3Parser.CountContext):
        super().exitCount(ctx)

    def enterReflection(self, ctx: Ah3Parser.ReflectionContext):
        super().enterReflection(ctx)

    def exitReflection(self, ctx: Ah3Parser.ReflectionContext):
        super().exitReflection(ctx)

    def enterInject(self, ctx: Ah3Parser.InjectContext):
        super().enterInject(ctx)

    def exitInject(self, ctx: Ah3Parser.InjectContext):
        super().exitInject(ctx)

    def enterAtom(self, ctx: Ah3Parser.AtomContext):
        super().enterAtom(ctx)

    def exitAtom(self, ctx: Ah3Parser.AtomContext):
        super().exitAtom(ctx)

    def enterAtom_obj_dict(self, ctx: Ah3Parser.Atom_obj_dictContext):
        super().enterAtom_obj_dict(ctx)

    def exitAtom_obj_dict(self, ctx: Ah3Parser.Atom_obj_dictContext):
        super().exitAtom_obj_dict(ctx)

    def enterAtom_obj_list(self, ctx: Ah3Parser.Atom_obj_listContext):
        super().enterAtom_obj_list(ctx)

    def exitAtom_obj_list(self, ctx: Ah3Parser.Atom_obj_listContext):
        super().exitAtom_obj_list(ctx)

    def enterAtom_string(self, ctx: Ah3Parser.Atom_stringContext):
        super().enterAtom_string(ctx)

    def exitAtom_string(self, ctx: Ah3Parser.Atom_stringContext):
        super().exitAtom_string(ctx)

    def enterAtom_number(self, ctx: Ah3Parser.Atom_numberContext):
        super().enterAtom_number(ctx)

    def exitAtom_number(self, ctx: Ah3Parser.Atom_numberContext):
        super().exitAtom_number(ctx)

    def enterAtom_boolean(self, ctx: Ah3Parser.Atom_booleanContext):
        super().enterAtom_boolean(ctx)

    def exitAtom_boolean(self, ctx: Ah3Parser.Atom_booleanContext):
        super().exitAtom_boolean(ctx)

    def enterAtom_hex(self, ctx: Ah3Parser.Atom_hexContext):
        super().enterAtom_hex(ctx)

    def exitAtom_hex(self, ctx: Ah3Parser.Atom_hexContext):
        super().exitAtom_hex(ctx)

    def enterAtom_none(self, ctx: Ah3Parser.Atom_noneContext):
        super().enterAtom_none(ctx)

    def exitAtom_none(self, ctx: Ah3Parser.Atom_noneContext):
        super().exitAtom_none(ctx)