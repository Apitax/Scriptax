from __future__ import annotations

from scriptax.grammar.build.Ah4Parser import Ah4Parser as AhParser, Ah4Parser
from scriptax.grammar.build.Ah4Visitor import Ah4Visitor as AhVisitorOriginal
from scriptax.drivers.Driver import Driver
from scriptax.models.Parameter import Parameter
from scriptax.models.Attributes import Attributes
from scriptax.models.AhOptions import AhOptions
from scriptax.models.BlockStatus import BlockStatus

from scriptax.parser.utils.BoilerPlate import generate_parse_tree, read_file, read_string, customizable_tree_parser

from scriptax.parser.SymbolTable import SymbolTable, ExtendedImport, create_table, Import
from scriptax.parser.symbols.SymbolScope import SymbolScope, SCOPE_GLOBAL, SCOPE_MODULE
from scriptax.parser.symbols.Symbol import Symbol, DATA_NUMBER, DATA_BOOLEAN, DATA_HEX, DATA_NONE, DATA_STRING, \
    DATA_DICT, DATA_LIST, DATA_METHOD, DATA_THREAD, DATA_PYTHONIC, DATA_INSTANCE, SYMBOL_VAR, SYMBOL_MODULE

from commandtax.models.Command import Command

from apitaxcore.models.State import State
from apitaxcore.models.Options import Options
from apitaxcore.utilities.Async import GenericExecution
from apitaxcore.utilities.Json import isJson
from apitaxcore.flow.LoadedDrivers import LoadedDrivers
from apitaxcore.flow.responses.ApitaxResponse import ApitaxResponse

import json
import re
import threading
import traceback

from typing import Tuple, Any, List, Union, Dict


# TODO: SCOPE GENERATION:
#   basic symbol creators:
#     assignment
#     sig_statement
#
#   symbol value adjusters:
#     assignment
#
#   symbol type adjusters/verifiers:
#     assignment
#
#   scope creators:
#     method_statement (ADD SYMBOL TO GLOBAL SCOPE & ADD AS CHILD SCOPE OF TYPE METHOD)
#     block            (ADD AS CHILD SCOPE OF TYPE BLOCK)
#     callback_block   (ADD AS CHILD SCOPE OF TYPE CALLBACK)
#
#     run recursively when encountering and merge into global scope:
#       extends_statement  (MERGE SCOPES & SYMBOLS INTO GLOBAL OF SUB SCRIPT PRIOR TO CURRENT SCRIPT)
#       import_statement   (ADD AS SCRIPT SYMBOL TYPE INTO GLOBAL SCOPE)
#
#   Scope ordering: imports, program path
#
# TODO: Variable access in DOT notation (dict, list, symbol, straight up data)
# TODO: Variable setting in DOT notation (dict, list, symbol, straight up data)
# TODO: Async, Await
#
# TODO: Combine class attributes: parser `state`, `status`, and `message` into a single dict
# TODO: Parameters must be injected into the symbol scope
#
# TODO: Support parameters when creating a new instance. myvar = new strings(param1="val1", param2="val2");
# TODO: Support builder pattern when creating a new instance. myvar = new strings(param1="val1", param2="val2").doSomeAction().doSomeOtherAction();
#
#

class AhVisitor(AhVisitorOriginal):
    """
    Parses and executes Scriptax code

    ...

    Attributes
    ----------
    log : Logger
        Logging class used to log messages
    config : Config
        Config class for retrieving configuration values
    appOptions : Options
        Application options such as debug mode
    parameters : dict
        Parameters sent to the parser. Typically method or constructor arguments
    state : dict
        Holds the state of execution. This includes the current file name, line, and character number of execution
    parser : Antlr4 Ctx Parser, deprecated
        The parser object created by Antlr4
    options : dict, deprecated
        Holds the options defined by the 'options' code in Scriptax
    status : str
        The current status of parsing. ok -> running properly, error -> the parsing has error'd, return -> the parser has completed and returned, exit -> unused
    message : str
        A message associated with the status. This allows the parser to provide an error message etc.
    symbol_table : SymbolTable
        The symbol table used for parsing
    regexVar : str
        The regex used for detecting mustache syntax
    """

    def __init__(self, parameters: List[Parameter] = None, options: Options = None, file=None,
                 symbol_table: SymbolTable = None):
        """
        Parameters
        ----------
        parameters : dict
            Parameters sent to the parser. Typically method or constructor arguments
        options : Options
            Application options such as debug mode
        file : str
            The file path + name
        symbol_table : SymbolTable
            If we would like to parse off of an existing symbol table
        """

        # Aliases
        self.log = State.log
        self.config = State.config

        # Parameters
        self.appOptions: Options = options if options is not None else Options()
        # self.appOptions.debug = True
        self.parameters: List[Parameter] = parameters if parameters is not None else []

        # TODO: Evaluate necessity of these
        self.state = {'file': file, 'line': 0, 'char': 0}
        self.parser = None
        self.options: AhOptions = AhOptions()

        # Parsing status
        # Values: ok, error, exit, return
        self.status = 'ok'
        self.message = ''

        # Symbol Table
        if not symbol_table:
            self.symbol_table: SymbolTable = SymbolTable(name="program", type=SCOPE_GLOBAL)
        else:
            self.symbol_table: SymbolTable = symbol_table

        # Used for mustache syntax dynamic replacement
        self.regexVar = '{{[ ]{0,}[A-z0-9_$.\-]{1,}[ ]{0,}}}'

    # TODO: Find a way to incorporate this into a parser status field
    # Sets the program into error mode
    def error(self, message):
        self.message = message
        self.status = 'error'

    def setStatusReturn(self):
        self.status = 'return'

    def setStatusExit(self):
        self.status = 'exit'

    def setStatusOk(self):
        self.status = 'ok'

    def isOk(self):
        return self.status == 'ok'

    def isError(self):
        return self.status == 'error'

    def isExit(self):
        return self.status == 'exit'

    def isReturn(self):
        return self.status == 'return'

    def parseScript(self, scriptax: str, parameters: dict = None) -> Tuple[Any, AhVisitor]:
        """
        Helper method which executes a given scriptax string

        Parameters
        ----------
        scriptax : str
            The scriptax code to execute
        parameters : dict
            The parameters we wish to execute with

        Returns
        -------
        Tuple[Any, AhVisitor]
            The first index is the returned result, the second is the parsing class
        """
        from scriptax.parser.utils.BoilerPlate import customizable_parser
        result = customizable_parser(scriptax, parameters=parameters)
        if result[1].isError():
            self.error(message=result[1].message)
            return None, None
        return result

    def parseScriptCustom(self, context, symbol_table: SymbolTable = None) -> Tuple[Any, AhVisitor]:
        """
        Helper method which executes on a given context with a given set of symbols

        Parameters
        ----------
        context : antlr 4 context
            The antlr 4 context variable
        symbol_table : SymbolTable
            The symbol table we wish to execute with

        Returns
        -------
        Tuple[Any, AhVisitor]
            The first index is the returned result, the second is the parsing class
        """
        from scriptax.parser.utils.BoilerPlate import customizable_context_parser
        result = customizable_context_parser(context, symbol_table=symbol_table)
        if result[1].isError():
            self.error(message=result[1].message)
            return None, None
        return result

    def set_state(self, file: str = None, line: int = None, char: int = None):
        """
        Sets the current state of the parser
        """
        if file:
            self.state['file'] = file
        if line:
            self.state['line'] = line
        if char:
            self.state['char'] = char

    def resolve_label(self, label):
        """
        Resolves a name
        """
        name = label
        if not isinstance(name, str):
            name = self.visit(label)
        return name

    # TODO
    def execute_os(self):
        """
        Executes an OS line
        """
        pass

    # TODO: This needs to be redone
    def execute_command(self, command: Command) -> ApitaxResponse:
        """
        Executes commandtax
        """
        from commandtax.flow.Connector import Connector
        if self.appOptions.debug:
            self.log.log('> Executing Commandtax: \'' + command.command + '\' ' + 'with parameters: ' + str(
                command.parameters))
            self.log.log('')

        if not command.options:
            command.options = self.appOptions

        if not command.options:
            command.options = Options()

        connector = Connector(options=command.options, credentials=command.credentials,
                              command=command.command, parameters=command.parameters, request=command.request)
        return connector.execute()

    # TODO: this needs to be redone
    def execute_callback(self, callback=None, response: ApitaxResponse = None, result=None):
        """
        Executes a callback
        """
        # from scriptax.parser.utils.BoilerPlate import customizableContextParser
        # table = SymbolTable()
        # if not result:
        #     result = response.getResponseBody()
        # elif response:
        #     result = {'result': result, 'response': response}

        # table.putSymbol(Symbol(name='result', symbolType=SYMBOL_VARIABLE, value=result))
        # for key, value in callback['params'].items():
        #     table.putSymbol(Symbol(name=key, symbolType=SYMBOL_VARIABLE, value=value))
        # # Returns the value found in any return statement within the callback.
        # # If no return statement is in the callback this will be None
        # return customizableContextParser(context=callback['block'], symbol_table=table, options=self.appOptions)[0][1]
        pass

    # TODO exceptions
    def set_variable(self, label, value=None):
        """
        Sets the value of a variable. Creates the variable if it does not exist yet.
        """
        label = self.resolve_label(label)
        self.symbol_table.set_symbol(name=label, value=value)

    # TODO exceptions
    def get_variable(self, label=None):
        """
        Gets the value of a variable. Raises an exception if that variable does not exist.
        """
        label = self.resolve_label(label)
        return self.symbol_table.get_symbol(name=label)
        # if convert:
        #     label = self.visit(label)
        # try:
        #     return self.getSymbol(label, False).value
        # except:
        #     self.error(message="Symbol `" + label + "` not found in scope `" + self.symbol_table.current.name + "`")
        #     return None

    # TODO exceptions
    def delete_variable(self, label):
        """

        """
        label = self.resolve_label(label)
        self.symbol_table.remove_symbol(name=label)

    def get_symbol(self, label) -> Symbol:
        """
        :param label:
        :return:
        """
        label = self.resolve_label(label)
        try:
            return self.symbol_table.get_symbol(name=label, as_value=False)
        except Exception:
            try:
                return self.symbol_table.get_symbol(name=label, type=SYMBOL_MODULE, as_value=False)
            except Exception:
                raise Exception("Could not find symbol")

    def import_module_file(self, path: str, driver=None, as_label=None):
        """

        :param path:
        :param driver:
        :param as_label:
        :return:
        """
        # Avoids circular dependencies
        from scriptax.parser.ModuleVisitor import ModuleParser

        driver = self.resolve_label(driver)
        as_label = self.resolve_label(as_label)

        driver_instance: Driver = LoadedDrivers.getPrimaryDriver()
        if driver:
            driver_instance = LoadedDrivers.getDriver(driver)

        scriptax = driver_instance.getDriverScript(path)
        tree = generate_parse_tree(read_string(scriptax))

        import_table = SymbolTable(name=as_label + "_import")
        module_parser = ModuleParser(symbol_table=import_table)
        module_parser.visit(tree)
        module = Import(tree=tree, scope=module_parser.symbol_table.scope())
        self.symbol_table.import_module(name=as_label, module=module)

    def import_module_string(self, label, scriptax: str):
        """

        :param label:
        :param scriptax:
        :return:
        """
        # Avoids circular dependencies
        from scriptax.parser.ModuleVisitor import ModuleParser

        label = self.resolve_label(label)
        tree = generate_parse_tree(read_string(scriptax))
        import_table = SymbolTable(name=label + "_import")
        module_parser = ModuleParser(symbol_table=import_table)
        module_parser.visit(tree)
        module = Import(tree=tree, scope=module_parser.symbol_table.scope())
        self.symbol_table.import_module(name=label, module=module)

    def extend(self, import_name):
        """

        """
        import_name = self.resolve_label(import_name)
        module: Import = self.symbol_table.extends(import_name=import_name)
        module_table = create_table(module.scope)
        customizable_tree_parser(tree=module.tree, symbol_table=module_table, options=self.options)
        # never call the constructor here. never ever ever

    def implements(self, label):
        """

        """
        label = self.resolve_label(label)
        self.symbol_table.implements(import_name=label)

    def new_instance(self, import_name, parameters: List[Parameter] = None) -> SymbolScope:
        """

        """
        import_name = self.resolve_label(import_name)
        instance: Import = self.symbol_table.new_instance(import_name=import_name)
        instance_table = create_table(instance.scope)
        customizable_tree_parser(tree=instance.tree, symbol_table=instance_table, options=self.options,
                                 parameters=parameters)
        # TODO : Call constructor if it exists
        return instance.scope

    def register_method(self, label, body_context, static=False):
        """

        """
        label = self.resolve_label(label)
        self.symbol_table.register_method(name=label, body_context=body_context, static=static)

    def execute_method(self, label, parameters: List[Parameter]):
        """

        """
        label = self.resolve_label(label)
        body_context = self.symbol_table.execute(name=label, parameters=parameters)
        if not body_context:
            # TODO: This should throw exception
            self.symbol_table.complete_execution()
            return None
        result = self.visit(body_context)
        self.symbol_table.complete_execution()
        return result

    def inject(self, line):
        """
        Dynamic mustache syntax injection
        """
        matches = re.findall(self.regexVar, line)
        for match in matches:
            label = match[2:-2].strip()
            replacer = self.getVariable(label, convert=False)
            line = line.replace(match, replacer)
        return line

    # TODO: Improve error message format
    def visitProg(self, ctx: AhParser.ProgContext):
        """
        Visit a parse tree produced by AhParser#prog.
        """
        self.symbol_table.enterScope()
        self.symbol_table.current.setMeta(name=self.state['file'], scopeType=SCOPE_SCRIPT)
        self.parser = ctx.parser
        result = self.visit(ctx.script_structure())

        if self.isError():
            self.log.error(
                self.message + ' in ' + str(self.state['file']) + ' @' + str(self.state['line']) + ':' + str(
                    self.state['char']))
            if self.appOptions.debug:
                self.log.log('')
                self.log.log('')
        self.symbol_table.exitScope()
        return result

    # Visit a parse tree produced by Ah4Parser#script_structure.
    def visitScript_structure(self, ctx: AhParser.Script_structureContext):
        self.visit(ctx.global_statements())
        self.visit(ctx.root_level_statements())
        return self.visit(ctx.statements())

    # Visit a parse tree produced by Ah4Parser#global_statements.
    def visitGlobal_statements(self, ctx: AhParser.Global_statementsContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by Ah4Parser#root_level_statements.
    def visitRoot_level_statements(self, ctx: AhParser.Root_level_statementsContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by AhParser#statements.
    def visitStatements(self, ctx: AhParser.StatementsContext) -> BlockStatus:
        i = 0
        while ctx.statement(i):
            result: tuple = self.visit(ctx.statement(
                i))  # First index of tuple is whether it is a return statement (bool), second is the statement result
            if result[0]:
                return result
            if self.isReturn() or self.isError():
                return False, None
            i += 1
        return False, None

    # Visit a parse tree produced by AhParser#statement.
    def visitStatement(self, ctx: AhParser.StatementContext) -> BlockStatus:
        debugTemp = self.appOptions.debug
        sensitiveTemp = self.appOptions.sensitive

        line = ctx.getText().strip()
        if line != "" and self.appOptions.debug:
            if ctx.NOT():
                self.log.log(
                    '> Now processing: (This lines contents has been hidden via the \'!\' operator. This is usually done to hide sensitive information)')
                self.log.log('')
                self.log.log('> Treating the rest of this statement as sensitive and disabling debug')
                self.log.log('')

                self.appOptions.debug = False
                self.appOptions.sensitive = True
            else:
                self.log.log('> Now processing: ' + line)
                self.log.log('')

        if ctx.terminated():
            temp = self.visit(ctx.terminated())
        else:
            temp = self.visit(ctx.non_terminated())

        if line != "" and self.appOptions.debug:
            self.log.log('')

        self.set_state(line=ctx.start.line)  # TODO: Try to add character here as well

        if ctx.NOT() and line != "" and debugTemp:
            self.log.log('> Setting debug and sensitive back to their original values')
            self.log.log('')
            self.log.log('')
            self.appOptions.debug = debugTemp
            self.appOptions.sensitive = sensitiveTemp

        return temp

    # Visit a parse tree produced by AhParser#terminated.
    def visitTerminated(self, ctx: AhParser.TerminatedContext) -> tuple:
        if ctx.return_statement():
            return True, self.visit(ctx.return_statement())
        return False, self.visitChildren(ctx)

    # Visit a parse tree produced by AhParser#non_terminated.
    def visitNon_terminated(self, ctx: AhParser.Non_terminatedContext) -> tuple:
        temp = self.visit(ctx.flow())
        return temp

    # Visit a parse tree produced by AhParser#executers.
    def visitExecute_statement(self, ctx: AhParser.Execute_statementContext):
        if ctx.execute():
            return self.visit(ctx.execute())
        if ctx.async_execute():
            thread = self.visit(ctx.async_execute())
            thread.start()
            return thread

    # Visit a parse tree produced by AhParser#expr.
    def visitExpr(self, ctx):

        if ctx.reflection():
            return self.visit(ctx.reflection())

        if ctx.create_instance():
            return self.visit(ctx.create_instance())

        if ctx.method_call():
            return self.visit(ctx.method_call())[0][1]

        if ctx.execute():
            return self.visit(ctx.execute())['result']

        if ctx.async_execute():
            return self.visit(ctx.async_execute())

        if ctx.atom():
            return self.visit(ctx.atom())

        if ctx.casting():
            return self.visit(ctx.casting())

        if ctx.auth_statement():
            return self.visit(ctx.auth_statement())

        if ctx.endpoint_statement():
            return self.visit(ctx.endpoint_statement())

        if ctx.count():
            return self.visit(ctx.count())

        if ctx.labels():
            return self.getVariable(ctx.labels())

        if ctx.inject():
            return self.visit(ctx.inject())

        if ctx.MINUS() and not ctx.expr(1):
            return self.visit(ctx.expr(0)) * -1

        if ctx.NOT():
            return not self.visit(ctx.expr(0))

        try:
            if ctx.AND():
                return self.visit(ctx.expr(0)) and self.visit(ctx.expr(1))

            if ctx.OR():
                return self.visit(ctx.expr(0)) or self.visit(ctx.expr(1))

            if ctx.EQ():
                return self.visit(ctx.expr(0)) == self.visit(ctx.expr(1))

            if ctx.NEQ():
                return self.visit(ctx.expr(0)) != self.visit(ctx.expr(1))

            if ctx.GE():
                return self.visit(ctx.expr(0)) >= self.visit(ctx.expr(1))

            if ctx.LE():
                return self.visit(ctx.expr(0)) <= self.visit(ctx.expr(1))

            if ctx.GT():
                return self.visit(ctx.expr(0)) > self.visit(ctx.expr(1))

            if ctx.LT():
                return self.visit(ctx.expr(0)) < self.visit(ctx.expr(1))
        except:
            stacktrace = traceback.format_exc(limit=0)
            self.error(("While evaluating expression with `" + str(
                self.visit(ctx.expr(0))) + "` and `" + str(self.visit(ctx.expr(1))) + "`: " + stacktrace).replace('\r',
                                                                                                                  '').replace(
                '\n', ''))

        if ctx.LPAREN():
            return self.visit(ctx.expr(0))

        if ctx.POW():
            return self.visit(ctx.expr(0)) ** self.visit(ctx.expr(1))

        if ctx.PLUS():
            left = self.visit(ctx.expr(0))
            right = self.visit(ctx.expr(1))
            if (isinstance(left, str) and not isinstance(right, str)) or (
                    isinstance(right, str) and not isinstance(left, str)):
                left = str(left)
                right = str(right)
                if self.appOptions.debug:
                    self.log.log('> Implicit cast to string: \'' + left + '\' + \'' + right + '\'')
                    self.log.log('')
            return left + right

        if ctx.MINUS():
            return self.visit(ctx.expr(0)) - self.visit(ctx.expr(1))

        if ctx.MUL():
            return self.visit(ctx.expr(0)) * self.visit(ctx.expr(1))

        if ctx.DIV():
            return self.visit(ctx.expr(0)) / self.visit(ctx.expr(1))

        return self.visitChildren(ctx)

    # Visit a parse tree produced by AhParser#flow.
    def visitFlow(self, ctx: AhParser.FlowContext) -> tuple:
        if ctx.if_statement():
            return self.visit(ctx.if_statement())
        if ctx.while_statement():
            return self.visit(ctx.while_statement())
        if ctx.for_statement():
            return self.visit(ctx.for_statement())

    # Visit a parse tree produced by Ah4Parser#method_statement.
    def visitMethod_statement(self, ctx: AhParser.Method_statementContext):
        self.symbol_table.current.addSymbol(
            symbol=Symbol(name=self.visit(ctx.label()), symbolType=SYMBOL_METHOD, dataType=DATA_CONTEXT,
                          value=ctx))
        # return self.visitChildren(ctx)

    # Visit a parse tree produced by Ah4Parser#method_call.
    def visitMethod_call(self, ctx: AhParser.Method_callContext) -> tuple:
        # TODO: Check to see whether ASYNC should be used here and if so execute in thread

        label = self.visit(ctx.labels())
        labels = label.split('.')

        context: AhParser.Method_statementContext = None  # ANTLR context of the method
        scope: SymbolScope = None  # Scope to execute the block within

        # print(self.getSymbol(label=label, symbolType=SYMBOL_METHOD, convert=False).getSymbolDebug())

        # Gathering the correct context and scope
        if len(labels) == 1:
            # Executing a method on the current scope
            scope = self.symbol_table.current
            # This is so that method calls inside of methods don't become child scopes of the calling method
            # Weird things happen if method scopes are children of method scopes
            if scope.parent.type == SCOPE_METHOD:
                scope = scope.parent.parent
            context = self.symbol_table.getSymbol(name=labels[0]).value
            if not context:
                self.error(message="Method not found:" + labels[0])
                return None, None
        elif len(labels) == 2:
            # Executing a method on an instance variable or imported script
            scope = self.symbol_table.getSymbol(name=labels[0]).value
            if not scope:
                self.error(message="Symbol not found:" + labels[0])
                return None, None
            context = createTableFromScope(scope).getSymbol(name=labels[1]).value
            if not context:
                self.error(message="Method not found:" + labels[1])
                return None, None
        else:
            self.error(message="Method chaining is not supported yet")

        expectedParameters = self.visit(context.sig_parameter_block())
        parameters = self.visit(ctx.optional_parameters_block())

        invertedExpectedParameters = []

        # Checking to ensure parameters are correct and filling in optional parameters where necessary
        for expected in expectedParameters:
            key = expected['label']
            invertedExpectedParameters.append(key)
            required = False
            if 'value' not in expected:
                required = True
            if key not in parameters and required:
                self.error(message="Required parameter not found in parameter list: " + key)
                return None, None
            if key not in parameters:
                parameters[key] = expected['value']

        # Creating the symbol table to execute the context within
        table: SymbolTable = createTableFromScope(scope)
        table.deleteOnExit = True  # Prevents hanging method & block scopes when debugging
        table.enterScope()
        table.current.setMeta(scopeType=SCOPE_METHOD)
        table.current.variableScanBlocked = True

        # Adding parameters as symbols
        for key, value in parameters.items():
            if key not in invertedExpectedParameters:
                self.error(message="Unexpected parameter passed to method: " + key)
                return None, None
            else:
                table.putSymbol(symbol=Symbol(name=key, symbolType=SYMBOL_VARIABLE, value=value))

        result = self.parseScriptCustom(context.block(), table)
        table.exitScope()
        # self.symbol_table.exitScopeAndDelete()  # This way we dont get a bunch of hanging method scopes when we debug
        return result

    # Visit a parse tree produced by AhParser#if_statement.
    def visitIf_statement(self, ctx: AhParser.If_statementContext) -> tuple:
        i = 0
        while True:
            if ctx.condition(i) is None:
                if ctx.ELSE():
                    return self.visit(ctx.block(i))
                else:
                    return False, None
            condition = self.visit(ctx.condition(i))
            if condition:
                return self.visit(ctx.block(i))
            else:
                i += 1

    # Visit a parse tree produced by AhParser#while_statement.
    def visitWhile_statement(self, ctx: AhParser.While_statementContext) -> tuple:
        while self.visit(ctx.condition()):
            result = self.visit(ctx.block())
            if result[0]:
                return result
        return False, None

    # Visit a parse tree produced by AhParser#for_statement.
    def visitFor_statement(self, ctx: AhParser.For_statementContext) -> tuple:
        clause = self.visit(ctx.expr())
        label = self.visit(ctx.labels())

        if isinstance(clause, str) and isJson(clause):
            clause = json.loads(clause)

        if isinstance(clause, list):
            if self.appOptions.debug:
                self.log.log('> Looping through list with var ' + label)
                self.log.log('')
            for item in clause:
                if self.appOptions.debug:
                    self.log.log('>> Assigning ' + label + ' = ' + str(item))
                    self.log.log('')
                    self.log.log('')
                self.setVariable(label=label, value=item, convert=False)
                result = self.visit(ctx.block())
                if result[0]:
                    return result
            self.deleteVariable(label=label, convert=False)

        elif isinstance(clause, float) or isinstance(clause, int):
            if self.appOptions.debug:
                self.log.log('> Looping through range with var ' + label)
                self.log.log('')
            for i in range(0, int(clause)):
                if self.appOptions.debug:
                    self.log.log('>> Assigning ' + label + ' = ' + str(i))
                    self.log.log('')
                    self.log.log('')
                self.setVariable(label=label, value=i, convert=False)
                result = self.visit(ctx.block())
                if result[0]:
                    return result
            self.deleteVariable(label=label, convert=False)

        else:
            if self.appOptions.debug:
                self.error('Invalid Loop Type: ' + str(type(clause)))
                self.log.log('')
        return False, None

    # Visit a parse tree produced by AhParser#each_statement.
    def visitEach_statement(self, ctx: AhParser.Each_statementContext):
        clause = self.visit(ctx.expr())

        if isinstance(clause, str) and isJson(clause):
            clause = json.loads(clause)

        if isinstance(clause, list):
            if self.appOptions.debug:
                self.log.log('> Looping through result')
                self.log.log('')
            callback = self.visit(ctx.callback())
            for item in clause:
                if self.appOptions.debug:
                    self.log.log('>> Assigning result = ' + str(item))
                    self.log.log('')
                    self.log.log('')
                self.execute_callback(callback=callback, result=item)
        else:
            self.error("An each loop must be passed a list")



    # Visit a parse tree produced by AhParser#callback.
    def visitCallback(self, ctx: AhParser.CallbackContext):
        parameters = {}
        if ctx.optional_parameters_block():
            parameters = self.visit(ctx.optional_parameters_block())
        return {"params": parameters, "block": ctx.callback_block()}

    # Visit a parse tree produced by AhParser#callback_block.
    def visitCallback_block(self, ctx: AhParser.Callback_blockContext):
        return self.visit(ctx.statements())

    # Visit a parse tree produced by AhParser#call_parameter.
    def visitCall_parameter(self, ctx: AhParser.Call_parameterContext):
        if ctx.expr():
            return {"value": self.visit(ctx.expr())}
        else:
            return self.visit(ctx.optional_parameter())

    # Visit a parse tree produced by AhParser#execute.
    def visitExecute(self, ctx):
        resolvedCommand = self.visit(ctx.commandtax())
        strict = resolvedCommand['strict']

        command = Command(command=resolvedCommand['command'], parameters=resolvedCommand['parameters'],
                          credentials=resolvedCommand['credentials'])

        response: ApitaxResponse = self.execute_command(command)

        if strict and not response.isStatusSuccess():
            self.error('Request returned non-success status code while in strict mode. Request returned: Status ' +
                       str(
                           response.getResponseStatusCode()) + ' ' + str(response.getResponseBody()))
            return None

        result = response.getResponseBody()

        if ctx.callback():
            callback = self.visit(ctx.callback())
            result = self.execute_callback(callback=callback, response=response)

        return dict({"command": command, "commandHandler": response, "result": result})

    def visitAtom(self, ctx: AhParser.AtomContext):

        if ctx.atom_obj_dict():
            return self.visit(ctx.atom_obj_dict())

        if ctx.atom_obj_list():
            return self.visit(ctx.atom_obj_list())

        if ctx.atom_obj_enum():
            return self.visit(ctx.atom_obj_enum())

        if ctx.atom_string():
            return self.visit(ctx.atom_string())

        if ctx.atom_number():
            return self.visit(ctx.atom_number())

        if ctx.atom_boolean():
            return self.visit(ctx.atom_boolean())

        if ctx.atom_hex():
            return self.visit(ctx.atom_hex())

        if ctx.atom_none():
            return self.visit(ctx.atom_none())

    def visitCase_statement(self, ctx: AhParser.Case_statementContext):
        return super().visitCase_statement(ctx)

    def visitDefault_statement(self, ctx: AhParser.Default_statementContext):
        return self.visit(ctx.block())

    # Visit a parse tree produced by AhParser#block.
    def visitBlock(self, ctx: AhParser.BlockContext) -> BlockStatus:
        self.symbol_table.enter_block_scope()
        if ctx.statements():
            result = self.visit(ctx.statements())
        else:
            result = self.visit(ctx.statement())
        self.symbol_table.exit_block_scope()
        return result

    def visitDone_statement(self, ctx: Ah4Parser.Done_statementContext) -> bool:
        return True

    def visitContinue_statement(self, ctx: Ah4Parser.Continue_statementContext) -> bool:
        return True

    def visitLog_statement(self, ctx: AhParser.Log_statementContext):
        if ctx.expr():
            self.log.log('> Logging: ' + json.dumps(self.visit(ctx.expr())))
            self.log.log('')

    def visitFlexible_parameter_block(self, ctx: AhParser.Flexible_parameter_blockContext) -> List[Parameter]:
        parameters: List[Parameter] = []
        i = 0
        while ctx.flexible_parameter(i):
            parameters.append(self.visit(ctx.flexible_parameter(i)))
            i += 1
        return parameters

    def visitFlexible_parameter(self, ctx: AhParser.Flexible_parameterContext) -> Parameter:
        if ctx.required_parameter():
            return self.visit(ctx.required_parameter())
        if ctx.optional_parameter():
            return self.visit(ctx.optional_parameter())

    def visitImport_statement(self, ctx: AhParser.Import_statementContext):
        labelIndex = 0
        driver = None
        if ctx.FROM():
            driver = self.visit(ctx.label(0))
            labelIndex += 1

        path = self.visit(ctx.labels())

        name = None
        if ctx.AS():
            name = self.visit(ctx.label(labelIndex))
        else:
            name = path.split('.')[-1]

        path = path.replace('.', '/') + '.ah'

        self.import_module_file(path=path, driver=driver, as_label=name)

    def visitExtends_statement(self, ctx: AhParser.Extends_statementContext):
        if not ctx.WITH():
            # Inheritance only
            self.extend(import_name=self.resolve_label(ctx.label(0)))
        else:
            label_count = 0
            comma_count = 0

            while ctx.label(label_count):
                label_count += 1

            while ctx.label(comma_count):
                comma_count += 1

            i = 0
            if label_count > (comma_count + 1):
                # If the first label is for inheritance
                self.extend(self.resolve_label(ctx.label(0)))
                i = 1

            while ctx.label(i):
                self.implements(self.resolve_label(ctx.label(i)))
                i += 1

    def visitCreate_instance(self, ctx: AhParser.Create_instanceContext):
        label = self.visit(ctx.label())

        parameters = self.visit(ctx.optional_parameters_block())

        return self.new_instance(import_name=label, parameters=parameters)

    def visitAhoptions_statement(self, ctx: AhParser.Ahoptions_statementContext):
        data = self.visit(ctx.atom_obj_dict())
        self.options = AhOptions(**data)

    def visitOptional_parameters_block(self, ctx: AhParser.Optional_parameters_blockContext) -> List[Parameter]:
        i = 0
        parameters: List[Parameter] = []
        while ctx.optional_parameter(i):
            parameters.append(self.visit(ctx.optional_parameter(i)))
            i += 1

        i = 0
        while ctx.dict_signal(i):
            parameters += self.visit(ctx.dict_signal(i))
            i += 1
        return parameters

    def visitOptional_parameter(self, ctx: AhParser.Optional_parameterContext) -> Parameter:
        return Parameter(name=self.visit(ctx.labels()), value=self.visit(ctx.expr()))

    def visitDict_signal(self, ctx: AhParser.Dict_signalContext) -> List[Parameter]:
        data = {}
        if ctx.labels():
            data = self.get_variable(label=ctx.labels())
        else:
            data = self.visit(ctx.atom_obj_dict())

        if not isinstance(data, dict):
            raise Exception("Not a dict")

        parameters: List[Parameter] = []
        for key, value in data.items():
            parameters.append(Parameter(name=key, value=value))

        return parameters

    # TODO: Support casting between enums and dicts
    def visitCasting(self, ctx: AhParser.CastingContext) -> Any:
        value = self.visit(ctx.expr())
        returner = None
        if ctx.TYPE_INT():
            returner = int(value)
            if self.appOptions.debug:
                self.log.log('> Explicitly Casting \'' + str(value) + '\' to int: ' + json.dumps(returner))
                self.log.log('')
            return returner

        if ctx.TYPE_DEC():
            returner = float(value)
            if self.appOptions.debug:
                self.log.log('> Explicitly Casting \'' + str(value) + '\' to number: ' + json.dumps(returner))
                self.log.log('')
            return returner

        if ctx.TYPE_BOOL():
            returner = bool(value)
            if self.appOptions.debug:
                self.log.log('> Explicitly Casting \'' + str(value) + '\' to boolean: ' + json.dumps(returner))
                self.log.log('')
            return returner

        if ctx.TYPE_STR():
            returner = str(value)
            if self.appOptions.debug:
                self.log.log('> Explicitly Casting \'' + str(value) + '\' to string: ' + json.dumps(returner))
                self.log.log('')
            return returner

        if ctx.TYPE_LIST():
            returner = list(str(value).split(","))
            if self.appOptions.debug:
                self.log.log('> Explicitly Casting \'' + str(value) + '\' to list: ' + json.dumps(returner))
                self.log.log('')
            return returner

        if ctx.TYPE_DICT():
            if isinstance(value, dict):
                returner = value
            elif isinstance(value, list):
                count = 0
                newdict = {}
                for i in value:
                    newdict.update({str(count): i})
                    count += 1
                returner = dict(newdict)
            elif isinstance(value, str) and isJson(value):
                returner = dict(json.loads(str(value)))
            else:
                returner = dict({"default": value})

            if self.appOptions.debug:
                self.log.log('> Explicitly Casting \'' + str(value) + '\' to dictionary: ' + json.dumps(returner))
                self.log.log('')

        return returner

    def visitAtom_obj_dict(self, ctx: AhParser.Atom_obj_dictContext) -> dict:
        dictionary = {}
        i = 0
        if ctx.COLON(0):
            dictionary[self.visit(ctx.expr(0))] = self.visit(ctx.expr(1))
        while ctx.COMMA(i) and ctx.expr((i + 1) * 2):
            base = (i + 1) * 2
            dictionary[self.visit(ctx.expr(base))] = self.visit(ctx.expr(base + 1))
            i += 1
        return dictionary

    def visitAssignment_statement(self, ctx: AhParser.Assignment_statementContext):
        label = self.visit(ctx.labels())
        value = None

        if ctx.expr():
            value = self.visit(ctx.expr())

        if not ctx.EQUAL():
            var = self.get_variable(label=label)
            if ctx.D_PLUS():
                value = var + 1
            elif ctx.D_MINUS():
                value = var - 1
            else:
                if ctx.PE():
                    value = var + value
                elif ctx.ME():
                    value = var - value
                elif ctx.MUE():
                    value = var * value
                elif ctx.DE():
                    value = var / value

        if ctx.SOPEN():
            var = self.get_variable(label=label)
            if not isinstance(var, list):
                self.error("Appending to a list requires the variable being a list")
                return
            var.append(value)
            tval = value
            value = var
            self.set_variable(label=label, value=value)
            if isinstance(tval, threading.Thread):
                tval.label = label + "." + str(len(value) - 1)
                tval.start()
        else:
            self.set_variable(label=label, value=value)
            if isinstance(value, threading.Thread):
                value.label = label
                value.start()

        if self.appOptions.debug:
            self.log.log('> Assigning Variable: ' + label + ' = ' + str(
                value))
            self.log.log('')

    def visitAtom_obj_list(self, ctx: AhParser.Atom_obj_listContext) -> list:
        parameters = []
        i = 0
        if ctx.expr(0):
            parameters.append(self.visit(ctx.expr(0)))
        while ctx.COMMA(i) and ctx.expr(i + 1):
            parameters.append(self.visit(ctx.expr(i + 1)))
            i += 1
        return parameters

    def visitAtom_obj_enum(self, ctx: AhParser.Atom_obj_enumContext) -> List[Parameter]:
        parameters: List[Parameter] = []
        i = 0
        if ctx.expr(0):
            # Using the arrow format
            if ctx.label(0):
                parameters.append(Parameter(name=self.visit(ctx.label(0)), value=self.visit(ctx.expr(0))))
            while ctx.COMMA(i) and ctx.label(i + 1):
                parameters.append(Parameter(name=self.visit(ctx.label(i + 1)), value=self.visit(ctx.expr(i + 1))))
                i += 1
        else:
            # Not using the arrow format
            if ctx.label(0):
                parameters.append(Parameter(name=self.visit(ctx.label(0)), value=i))
            while ctx.COMMA(i) and ctx.label(i + 1):
                parameters.append(Parameter(name=self.visit(ctx.label(i + 1)), value=i + 1))
                i += 1

        return parameters

    def visitError_statement(self, ctx: AhParser.Error_statementContext):
        message = "No error message was specified"
        if ctx.expr():
            message = self.visit(ctx.expr())
        self.error(message)

    def visitInject(self, ctx: AhParser.InjectContext):
        returner = self.visit(ctx.expr())
        if self.appOptions.debug:
            self.log.log('> Injecting into: ' + ctx.getText() + ' with the value ' + str(returner))
            self.log.log('')
        return returner

    def visitCondition(self, ctx: AhParser.ConditionContext):
        condition = self.visit(ctx.expr())

        if self.appOptions.debug:
            self.log.log('>> Evaluated Flow Condition as: ' + str(condition))
            self.log.log('')

        return condition

    def visitReturn_statement(self, ctx: AhParser.Return_statementContext) -> Any:
        exportation = None
        if ctx.expr():
            exportation = self.visit(ctx.expr())

        if self.appOptions.debug:
            if exportation:
                self.log.log('> Returning with value: ' + str(exportation))
            else:
                self.log.log('> Returning with value: None')
            self.log.log('')

        return exportation

    def visitCount(self, ctx: AhParser.CountContext) -> int:
        return len(self.visit(ctx.expr()))

    def visitDelete_statement(self, ctx: AhParser.Delete_statementContext):
        label = self.resolve_label(ctx.labels())
        self.delete_variable(label=label)
        if self.appOptions.debug:
            self.log.log('> Deleteing variable: ' + label)
            self.log.log('')

    def visitAwait_statement(self, ctx: AhParser.Await_statementContext):
        label = self.resolve_label(ctx.labels())
        var = self.get_variable(label=label)
        if isinstance(var, GenericExecution):
            var.join()
        return var

    def visitReflection(self, ctx: AhParser.ReflectionContext) -> dict:
        symbol = self.get_symbol(label=ctx.labels())
        return symbol.get_symbol_debug()

    def visitRequired_parameter(self, ctx: AhParser.Required_parameterContext) -> Parameter:
        label = self.resolve_label(ctx.labels())
        return Parameter(name=label)

    def visitLabels(self, ctx: AhParser.LabelsContext) -> str:

        label = [self.visit(ctx.label_comp(0))]
        i = 0
        while ctx.DOT(i):
            label.append(str(self.visit(ctx.label_comp(i + 1))))
            i += 1

        label = '.'.join(label)

        return label.replace('$', '')

    def visitLabel_comp(self, ctx: AhParser.Label_compContext) -> str:
        if ctx.label():
            return self.visit(ctx.label())
        else:
            return self.visit(ctx.inject())

    def visitLabel(self, ctx: AhParser.LabelContext) -> str:
        return ctx.LABEL().getText()

    def visitAttribute(self, ctx: AhParser.AttributeContext) -> Attributes:
        attributes = Attributes()
        if ctx.SCRIPT():
            attributes.script = True
        if ctx.STATIC():
            attributes.static = True
        if ctx.ASYNC():
            attributes.asynchronous = True
        return attributes

    def visitAtom_string(self, ctx: AhParser.Atom_stringContext) -> str:
        line = ctx.STRING().getText()[1:-1]
        line = line.replace('\\"', '"')
        line = line.replace('\\\'', '\'')
        matches = re.findall(self.regexVar, line)
        for match in matches:
            label = match[2:-2].strip()
            label = label.replace('$', '')
            replacer = str(self.get_variable(label))
            line = line.replace(match, replacer)
            if self.appOptions.debug:
                self.log.log('> Injecting Variable into String \'' + label + '\': ' + line)
                self.log.log('')
        return line

    def visitAtom_number(self, ctx: AhParser.Atom_numberContext) -> Union[int, float]:
        if ctx.INT():
            return int(ctx.INT().getText())
        else:
            return float(ctx.FLOAT().getText())

    def visitAtom_boolean(self, ctx: AhParser.Atom_booleanContext) -> bool:
        if ctx.TRUE():
            return True
        if ctx.FALSE():
            return False

    def visitAtom_hex(self, ctx: AhParser.Atom_hexContext):
        return '0x' + str(ctx.HEX().getText())[2:].upper()

    def visitAtom_none(self, ctx: AhParser.Atom_noneContext):
        return None

    def visitRunnable_statements(self, ctx: AhParser.Runnable_statementsContext):
        return super().visitRunnable_statements(ctx)

    def visitMethod_call_statement(self, ctx: AhParser.Method_call_statementContext):
        return super().visitMethod_call_statement(ctx)

    def visitCommandtax_statement(self, ctx: AhParser.Commandtax_statementContext):
        return super().visitCommandtax_statement(ctx)

    def visitOs_statement(self, ctx: AhParser.Os_statementContext):
        return super().visitOs_statement(ctx)

    def visitAtom_callback(self, ctx: AhParser.Atom_callbackContext):
        return super().visitAtom_callback(ctx)

    def visitMethod_def_atom(self, ctx: AhParser.Method_def_atomContext):
        return super().visitMethod_def_atom(ctx)

    def visitSwitch_statement(self, ctx: AhParser.Switch_statementContext):
        return super().visitSwitch_statement(ctx)










