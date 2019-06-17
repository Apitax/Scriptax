from __future__ import annotations

from scriptax.exceptions.SymbolNotFound import SymbolNotFound
from scriptax.exceptions.SymbolError import SymbolError
from scriptax.exceptions.InvalidSymbolAccess import InvalidSymbolAccess
from scriptax.exceptions.InvalidParameters import InvalidParameters
from scriptax.exceptions.InvalidExpression import InvalidExpression
from scriptax.exceptions.InvalidType import InvalidType
from scriptax.grammar.build.Ah4Parser import Ah4Parser as AhParser, Ah4Parser
from scriptax.grammar.build.Ah4Visitor import Ah4Visitor as AhVisitorOriginal
from scriptax.drivers.Driver import Driver
from scriptax.models.Parameter import Parameter
from scriptax.models.Attributes import Attributes
from scriptax.models.AhOptions import AhOptions
from scriptax.models.BlockStatus import BlockStatus
from scriptax.models.CaseStatus import CaseStatus
from scriptax.models.Callback import Callback

from scriptax.parser.utils.BoilerPlate import generate_parse_tree, read_file, read_string, customizable_tree_parser

from scriptax.parser.SymbolTable import SymbolTable, create_table, Import
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

from antlr4 import InputStream

from typing import Tuple, Any, List, Union


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
        The current status of parsing. ok -> running properly, error -> the parsing has error'd, return
            -> the parser has completed and returned, exit -> unused
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
        self.logger = State.log
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
            self.symbol_table: SymbolTable = SymbolTable(name="main", type=SCOPE_MODULE)
        else:
            self.symbol_table: SymbolTable = symbol_table

        # Used for mustache syntax dynamic replacement
        # self.regexVar = '{{[ ]{0,}[A-z0-9_$.\-]{1,}[ ]{0,}}}'
        self.regexVar = r"<\|[ ]{0,}[A-z0-9_$.\-]{1,}[ ]{0,}>"
        # Needs the r to indicate raw string to avoid escaping errors

    # TODO: Find a way to incorporate this into a parser status field
    # Sets the program into error mode
    def error(self, message):
        self.message = message
        self.status = 'error'

    def set_status_return(self):
        self.status = 'return'

    def set_status_exit(self):
        self.status = 'exit'

    def set_status_ok(self):
        self.status = 'ok'

    def is_ok(self):
        return self.status == 'ok'

    def is_error(self):
        return self.status == 'error'

    def is_exit(self):
        return self.status == 'exit'

    def is_return(self):
        return self.status == 'return'

    def log(self, message: str, no_linebreak: bool = False):
        """
        Logs a message to the log file and console
        Generally will add a line line break after the message, but if no_linebreak is true, it won't
        :param message:
        :param no_linebreak:
        :return:
        """
        if self.appOptions.debug:
            self.logger.log('> ' + message)
            if not no_linebreak:
                self.logger.log('')

    def log_br(self):
        """
        Adds a line break to the log file and the console
        :return:
        """
        if self.appOptions.debug:
            self.logger.log('')

    def parse_script(self, scriptax: str, parameters: dict = None) -> Tuple[Any, AhVisitor]:
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
        result = customizable_parser(scriptax, parameters=parameters, options=self.appOptions)
        if result[1].is_error():
            self.error(message=result[1].message)
            return None, None
        return result

    def parse_script_custom(self, context, symbol_table: SymbolTable = None) -> Tuple[Any, AhVisitor]:
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
        result = customizable_context_parser(context, symbol_table=symbol_table, options=self.appOptions)
        if result[1].is_error():
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
        self.log('Executing Commandtax: \'' + command.command + '\' ' + 'with parameters: ' + str(
            command.parameters))

        if not command.options:
            command.options = self.appOptions

        if not command.options:
            command.options = Options()

        connector = Connector(options=command.options, credentials=command.credentials,
                              command=command.command, parameters=command.parameters, request=command.request)
        return connector.execute()

    def execute_callback(self, callback: Callback = None, parameters: List[Parameter] = None) -> BlockStatus:
        """
        Executes a callback
        """
        self.symbol_table.execute(name=callback.name, parameters=parameters + callback.parameters, isolated_scope=True)
        if not callback.block:
            # TODO: This should throw exception
            self.symbol_table.complete_execution()
            return BlockStatus()
        result = self.visit(callback.block())
        self.symbol_table.complete_execution()
        return result

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
        Deletes a variable from the scope
        """
        label = self.resolve_label(label)
        self.symbol_table.remove_symbol(name=label)

    def get_symbol(self, label) -> Symbol:
        """
        Retrieves a symbol from the scope
        :param label:
        :return:
        """
        label = self.resolve_label(label)
        try:
            return self.symbol_table.get_symbol(name=label, as_value=False)
        except SymbolNotFound:
            try:
                return self.symbol_table.get_symbol(name=label, type=SYMBOL_MODULE, as_value=False)
            except SymbolNotFound:
                raise SymbolNotFound("Could not find symbol")

    def import_module_file(self, path: str, driver: str = None, as_label: str = None):
        """
        Imports a module file from a driver
        :param path:
        :param driver:
        :param as_label:
        :return:
        """
        # Avoids circular dependencies
        from scriptax.parser.ModuleVisitor import ModuleParser

        if as_label:
            as_label = self.resolve_label(as_label)

        driver_instance: Driver = LoadedDrivers.getPrimaryDriver()
        if driver:
            driver = self.resolve_label(driver)
            driver_instance = LoadedDrivers.getDriver(driver)

        scriptax: InputStream = driver_instance.getDriverScript(path)
        tree = generate_parse_tree(scriptax)

        import_table = SymbolTable(name=as_label + "_import")
        module_parser = ModuleParser(symbol_table=import_table)
        module_parser.visit(tree)
        module = Import(tree=tree, scope=module_parser.symbol_table.scope())
        self.symbol_table.import_module(name=as_label, module=module)

    def import_module_string(self, label, scriptax: str):
        """
        Imports Scriptax via a passed in string
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
        Extends the current static scope by another. This will do the linking and the execution of the extended scope.
        """
        import_name = self.resolve_label(import_name)
        module: Import = self.symbol_table.extends(import_name=import_name)
        module_table = create_table(module.scope)
        customizable_tree_parser(tree=module.tree, symbol_table=module_table, options=self.appOptions)
        # never call the constructor here. never ever ever
        # Instead the constructor should be called via super() from the child class

    def implements(self, label):
        """
        Adds any static methods from an interface into this scope
        """
        label = self.resolve_label(label)
        self.symbol_table.implements(import_name=label)

    def new_instance(self, import_name, parameters: List[Parameter] = None) -> SymbolScope:
        """
        Creates a new instance (Executes an import and put its SymbolScope into a symbol inside of the current scope
        """
        import_name = self.resolve_label(import_name)
        instance: Import = self.symbol_table.new_instance(import_name=import_name)
        instance_table = create_table(instance.scope)
        returned, visitor = customizable_tree_parser(tree=instance.tree, symbol_table=instance_table,
                                                     options=self.appOptions,
                                                     parameters=parameters)

        try:
            visitor.execute_method("self.construct", parameters=parameters)
        except SymbolNotFound:
            self.log("Didn't call constructor on new instance as it doesn't exist")
        return visitor.symbol_table.current

    def register_method(self, label, method_context, attributes: Attributes) -> Symbol:
        """
        Add a new method into the current scope
        """
        label = self.resolve_label(label)
        return self.symbol_table.register_method(name=label, method_context=method_context, attributes=attributes)

    def execute_method(self, label, parameters: List[Parameter]) -> BlockStatus:
        """
        Execute a method found inside of the current scope or any of its static parents going up the interface and inheritance tree
        """
        label = self.resolve_label(label)
        method_context: AhParser.Method_def_atomContext = self.symbol_table.execute(name=label, parameters=parameters)
        if not method_context:
            self.symbol_table.complete_execution()
            raise InvalidSymbolAccess(
                "Cannot execute something which is not a method " + label + ". Scriptax.Visitor@execute_method")

        # Add in optional parameters and verify that the two parameter lists (defined & passed) match
        parameter_names = []
        for parameter in parameters:
            parameter_names.append(parameter.name)
        defined_parameters = self.visit(method_context.flexible_parameter_block())
        defined_parameter_names = []

        # Check defined parameters against passed in parameters and add in optional ones
        for parameter in defined_parameters:
            if parameter.required and parameter.name not in parameter_names:
                raise InvalidParameters(
                    "Required parameter " + parameter.name + " not found in parameter list. Scriptax.Visitor@execute_method")
            if not parameter.required and parameter.name not in parameter_names:
                self.symbol_table.current.insert_symbol(Symbol(name=parameter.name, value=parameter.value))
            defined_parameter_names.append(parameter.name)

        # Check passed in parameters to ensure there aren't extra ones which were not defined
        for parameter in parameters:
            if parameter.name not in defined_parameter_names:
                raise InvalidParameters(
                    "Unexpected parameter " + parameter.name + ". Scriptax.Visitor@execute_method")

        # TODO: If async attribute is true, then this needs to be launched in a thread
        result = self.visit(method_context.block())
        self.symbol_table.complete_execution()
        return result

    def inject(self, line):
        """
        Dynamic mustache syntax injection
        """
        matches = re.findall(self.regexVar, line)
        for match in matches:
            label = match[2:-2].strip()
            replacer = self.get_variable(label)
            line = line.replace(match, replacer)
        return line

    # TODO: Improve error message format
    def visitProg(self, ctx: AhParser.ProgContext) -> BlockStatus:
        """
        Visit a parse tree
        """
        self.parser = ctx.parser
        result = self.visit(ctx.script_structure())

        if self.is_error():
            self.logger.error(
                self.message + ' in ' + str(self.state['file']) + ' @' + str(self.state['line']) + ':' + str(
                    self.state['char']))

            self.log_br()
            self.log_br()
        return result

    def visitScript_structure(self, ctx: AhParser.Script_structureContext) -> BlockStatus:
        self.visit(ctx.global_statements())
        self.visit(ctx.root_level_statements())
        return self.visit(ctx.statements())

    def visitGlobal_statements(self, ctx: AhParser.Global_statementsContext):
        return self.visitChildren(ctx)

    def visitRoot_level_statements(self, ctx: AhParser.Root_level_statementsContext):
        return self.visitChildren(ctx)

    def visitStatements(self, ctx: AhParser.StatementsContext) -> BlockStatus:
        i = 0
        while ctx.statement(i):
            result: BlockStatus = self.visit(ctx.statement(
                i))
            if result.returned or result.continued or result.done:
                return result
            if self.is_error():
                return BlockStatus()
            i += 1
        return BlockStatus()

    def visitStatement(self, ctx: AhParser.StatementContext) -> BlockStatus:
        debug_temp = self.appOptions.debug
        sensitive_temp = self.appOptions.sensitive

        line = ctx.getText().strip()
        if line != "" and self.appOptions.debug:
            if ctx.NOT():
                self.log(
                    'Now processing: (This lines contents has been hidden via the \'!\' operator. This is usually done to hide sensitive information)')
                self.log_br()
                self.log('Treating the rest of this statement as sensitive and disabling debug')

                self.appOptions.debug = False
                self.appOptions.sensitive = True
            else:
                self.log('Now processing: ' + line)

        if ctx.terminated():
            temp = self.visit(ctx.terminated())
        else:
            temp = self.visit(ctx.non_terminated())

        if line != "" and self.appOptions.debug:
            self.log_br()

        self.set_state(line=ctx.start.line)  # TODO: Try to add character here as well

        if ctx.NOT() and line != "" and debug_temp:
            self.log('Setting debug and sensitive back to their original values')
            self.appOptions.debug = debug_temp
            self.appOptions.sensitive = sensitive_temp

        return temp

    def visitExpr(self, ctx):
        # These need to be in order
        if ctx.reflection():
            return self.visit(ctx.reflection())

        if ctx.create_instance():
            return self.visit(ctx.create_instance())

        if ctx.runnable_statements():
            return self.visit(ctx.runnable_statements()).result

        if ctx.atom():
            return self.visit(ctx.atom())

        if ctx.casting():
            return self.visit(ctx.casting())

        if ctx.count():
            return self.visit(ctx.count())

        if ctx.labels():
            return self.get_variable(ctx.labels())

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
        except InvalidExpression:
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

            # Dictionary addition
            if isinstance(left, dict) and isinstance(right, dict):
                left.update(right)
                return left

            # Concatenating strings, and ez conversion of either side to string
            if (isinstance(left, str) and not isinstance(right, str)) or (
                    isinstance(right, str) and not isinstance(left, str)):
                left = str(left)
                right = str(right)
                if self.appOptions.debug:
                    self.log('Implicit cast to string: \'' + left + '\' + \'' + right + '\'')

            return left + right

        if ctx.MINUS():
            left = self.visit(ctx.expr(0))
            right = self.visit(ctx.expr(1))

            # List subtraction
            if isinstance(left, list) and isinstance(right, list):
                for item in right:
                    if item in left:
                        left.remove(item)
                return left

            # Dict subtraction
            if isinstance(left, dict) and isinstance(right, dict):
                for key, value in right.items():
                    if key in left:
                        del left[key]
                return left

            # Dict subtract list
            if isinstance(left, dict) and isinstance(right, list):
                for item in right:
                    if item in left:
                        del left[item]
                return left

            # Regular subtraction
            return left - right

        if ctx.MUL():
            return self.visit(ctx.expr(0)) * self.visit(ctx.expr(1))

        if ctx.DIV():
            return self.visit(ctx.expr(0)) / self.visit(ctx.expr(1))

        if ctx.PERCENT():
            return self.visit(ctx.expr(0)) % self.visit(ctx.expr(1))

        return self.visitChildren(ctx)

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

        if ctx.atom_callback():
            return self.visit(ctx.atom_callback())

        if ctx.method_def_atom():
            return self.visit(ctx.method_def_atom())

    def visitTerminated(self, ctx: AhParser.TerminatedContext) -> BlockStatus:
        if ctx.return_statement():
            return BlockStatus(returned=True, result=self.visit(ctx.return_statement()))
        if ctx.continue_statement():
            return BlockStatus(continued=True)
        if ctx.done_statement():
            return BlockStatus(done=True)
        return BlockStatus(result=self.visitChildren(ctx))

    def visitRunnable_statements(self, ctx: AhParser.Runnable_statementsContext) -> BlockStatus:
        # TODO: Must be changed to await threads where necessary
        # TODO: Spawn the thread here if saync is set
        result = BlockStatus()
        if ctx.method_call_statement():
            result = self.visit(ctx.method_call_statement())
        elif ctx.os_statement():
            result = self.visit(ctx.os_statement())
        elif ctx.commandtax_statement():
            result = self.visit(ctx.commandtax_statement())

        if ctx.atom_callback():
            callback = self.visit(ctx.atom_callback())
            self.execute_callback(callback=callback, parameters=[Parameter(name="result", value=result)])

        return result

    def visitMethod_call_statement(self, ctx: AhParser.Method_call_statementContext) -> BlockStatus:
        name = self.resolve_label(ctx.labels())
        parameters: List[Parameter] = self.visit(ctx.optional_parameters_block())
        return self.execute_method(label=name, parameters=parameters)

    # TODO
    def visitCommandtax_statement(self, ctx: AhParser.Commandtax_statementContext):
        return super().visitCommandtax_statement(ctx)

    # TODO
    def visitOs_statement(self, ctx: AhParser.Os_statementContext):
        return super().visitOs_statement(ctx)

    def visitEach_statement(self, ctx: AhParser.Each_statementContext):
        clause = self.visit(ctx.expr())

        if isinstance(clause, list):
            self.log('Looping through result')

            callback = self.visit(ctx.atom_callback())
            # TODO: Each of these callbacks must be executed in separate threads
            for item in clause:
                self.log('> Assigning result = ' + str(item))
                self.execute_callback(callback=callback, parameters=[Parameter(name="result", value=item)])
        else:
            self.error("An each loop must be passed a list")

    def visitAtom_callback(self, ctx: AhParser.Atom_callbackContext) -> Callback:
        callback: Callback = Callback(parameters=self.visit(ctx.optional_parameters_block()),
                                      block=ctx.callback_block())
        self.register_method(label=callback.name, method_context=callback.block, attributes=Attributes())
        return callback

    def visitCallback_block(self, ctx: AhParser.Callback_blockContext) -> BlockStatus:
        return self.visit(ctx.statements())

    def visitMethod_def_atom(self, ctx: AhParser.Method_def_atomContext) -> Symbol:
        attributes: Attributes = self.visit(ctx.attributes())
        label: str = self.resolve_label(ctx.label())
        return self.register_method(label=label, method_context=ctx, attributes=attributes)

    def visitNon_terminated(self, ctx: AhParser.Non_terminatedContext) -> BlockStatus:
        temp = self.visit(ctx.flow())
        return temp

    def visitFlow(self, ctx: AhParser.FlowContext) -> BlockStatus:
        if ctx.if_statement():
            return self.visit(ctx.if_statement())
        if ctx.switch_statement():
            return self.visit(ctx.switch_statement())
        if ctx.while_statement():
            return self.visit(ctx.while_statement())
        if ctx.for_statement():
            return self.visit(ctx.for_statement())

    def visitIf_statement(self, ctx: AhParser.If_statementContext) -> BlockStatus:
        i = 0
        while ctx.condition(i):
            if self.visit(ctx.condition(i)):
                return self.visit(ctx.block(i))
            i += 1

        if ctx.ELSE():
            return self.visit(ctx.block(i))

        return BlockStatus()

    def visitFor_statement(self, ctx: AhParser.For_statementContext) -> BlockStatus:
        clause = self.visit(ctx.expr())
        label = self.visit(ctx.labels())

        if isinstance(clause, list):
            self.log('Looping through list with var ' + label)

            for item in clause:
                self.log('> Assigning ' + label + ' = ' + str(item))

                self.symbol_table.enter_block_scope()
                self.set_variable(label=label, value=item)
                block_status: BlockStatus = self.visit(ctx.block())
                self.symbol_table.exit_block_scope()
                if block_status.returned:
                    return block_status
                elif block_status.done:
                    return BlockStatus()

        elif isinstance(clause, float) or isinstance(clause, int):
            self.log('Looping through range with var ' + label)

            for i in range(0, int(clause)):
                self.log('> Assigning ' + label + ' = ' + str(i))

                self.symbol_table.enter_block_scope()
                self.set_variable(label=label, value=i)
                block_status: BlockStatus = self.visit(ctx.block())
                self.symbol_table.exit_block_scope()
                if block_status.returned:
                    return block_status
                elif block_status.done:
                    return BlockStatus()

        else:
            self.error('Invalid Loop Type: ' + str(type(clause)))

        return BlockStatus()

    def visitWhile_statement(self, ctx: AhParser.While_statementContext) -> BlockStatus:
        while self.visit(ctx.condition()):
            block_status: BlockStatus = self.visit(ctx.block())
            if block_status.returned:
                return block_status
            elif block_status.done:
                return BlockStatus()
        return BlockStatus()

    def visitSwitch_statement(self, ctx: AhParser.Switch_statementContext) -> BlockStatus:
        i = 0
        while ctx.case_statement(i):
            case_status: CaseStatus = self.visit(ctx.case_statement(i))
            if case_status.executed and not case_status.continued:
                return BlockStatus(returned=case_status.returned, result=case_status.result)
            i += 1
        if ctx.default_statement():
            block_status: BlockStatus = self.visit(ctx.default_statement())
            block_status.continued = False
            block_status.done = False
            return block_status
        return BlockStatus()

    def visitCase_statement(self, ctx: AhParser.Case_statementContext) -> CaseStatus:
        case_status = CaseStatus()
        if self.visit(ctx.condition()):
            case_status = CaseStatus(**self.visit(ctx.block()).dict())
            case_status.executed = True
        return case_status

    def visitDefault_statement(self, ctx: AhParser.Default_statementContext) -> BlockStatus:
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
            self.log('Logging: ' + json.dumps(self.visit(ctx.expr())))

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

        label_index = 0
        driver = None
        if ctx.FROM():
            driver = self.visit(ctx.label(0))
            label_index += 1

        path = self.visit(ctx.labels())

        if ctx.AS():
            name = self.visit(ctx.label(label_index))
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

            while ctx.COMMA(comma_count):
                comma_count += 1

            i = 0
            if label_count > (comma_count + 1):
                # If the first label is for inheritance
                self.extend(import_name=self.resolve_label(ctx.label(0)))
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
        self.symbol_table.get_nearest_module().attributes.update(self.options.dict())

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
        return Parameter(name=self.visit(ctx.labels()), value=self.visit(ctx.expr()), required=False)

    def visitDict_signal(self, ctx: AhParser.Dict_signalContext) -> List[Parameter]:
        if ctx.labels():
            data = self.get_variable(label=ctx.labels())
        else:
            data = self.visit(ctx.atom_obj_dict())

        if not isinstance(data, dict):
            raise InvalidType("Not a dict")

        parameters: List[Parameter] = []
        for key, value in data.items():
            parameters.append(Parameter(name=key, value=value))

        return parameters

    # TODO: Support casting between enums and dicts
    def visitCasting(self, ctx: AhParser.CastingContext) -> Any:
        value = self.visit(ctx.expr())
        returner = None
        if ctx.TYPE_INT():
            returner = int(float(value))
            self.log('Explicitly Casting \'' + str(value) + '\' to int: ' + json.dumps(returner))
            return returner

        if ctx.TYPE_DEC():
            returner = float(value)
            self.log('Explicitly Casting \'' + str(value) + '\' to number: ' + json.dumps(returner))
            return returner

        if ctx.TYPE_BOOL():
            if isinstance(value, str):
                if value in ["false", "False", ""]:
                    returner = False
                else:
                    returner = True
            else:
                returner = bool(value)
            self.log('Explicitly Casting \'' + str(value) + '\' to boolean: ' + json.dumps(returner))
            return returner

        if ctx.TYPE_STR():
            returner = str(value)
            self.log('Explicitly Casting \'' + str(value) + '\' to string: ' + json.dumps(returner))
            return returner

        if ctx.TYPE_LIST():
            returner = list(str(value).split(","))
            self.log('Explicitly Casting \'' + str(value) + '\' to list: ' + json.dumps(returner))
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

            self.log('Explicitly Casting \'' + str(value) + '\' to dictionary: ' + json.dumps(returner))

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

        if isinstance(value, Symbol) and value.data_type == DATA_METHOD:
            self.register_method(label, method_context=value.value, attributes=Attributes(**value.attributes))
            return

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

        self.log('Assigning Variable: ' + label + ' = ' + str(value))

    def visitAtom_obj_list(self, ctx: AhParser.Atom_obj_listContext) -> list:
        parameters = []
        i = 0
        if ctx.expr(0):
            parameters.append(self.visit(ctx.expr(0)))
        while ctx.COMMA(i) and ctx.expr(i + 1):
            parameters.append(self.visit(ctx.expr(i + 1)))
            i += 1
        return parameters

    def visitAtom_obj_enum(self, ctx: AhParser.Atom_obj_enumContext) -> dict:
        parameters: dict = {}
        i = 0
        if ctx.expr(0):
            # Using the arrow format
            if ctx.label(0):
                parameters[self.visit(ctx.label(0))] = self.visit(ctx.expr(0))
            while ctx.COMMA(i) and ctx.label(i + 1):
                parameters[self.visit(ctx.label(i + 1))] = self.visit(ctx.expr(i + 1))
                i += 1
        else:
            # Not using the arrow format
            if ctx.label(0):
                parameters[self.visit(ctx.label(0))] = i
            while ctx.COMMA(i) and ctx.label(i + 1):
                parameters[self.visit(ctx.label(i + 1))] = i + 1
                i += 1

        return parameters

    def visitError_statement(self, ctx: AhParser.Error_statementContext):
        message = "No error message was specified"
        if ctx.expr():
            message = self.visit(ctx.expr())
        self.error(message)

    def visitInject(self, ctx: AhParser.InjectContext):
        returner = self.visit(ctx.expr())
        self.log('Injecting into: ' + ctx.getText() + ' with the value ' + str(returner))
        return returner

    def visitCondition(self, ctx: AhParser.ConditionContext) -> bool:
        condition = self.visit(ctx.expr())

        self.log('> Evaluated Flow Condition as: ' + str(condition))

        return bool(condition)

    def visitReturn_statement(self, ctx: AhParser.Return_statementContext) -> Any:
        exportation = None
        if ctx.expr():
            exportation = self.visit(ctx.expr())

        if exportation:
            self.log('Returning with value: ' + str(exportation))
        else:
            self.log('Returning with value: None')

        return exportation

    def visitCount(self, ctx: AhParser.CountContext) -> int:
        return len(self.visit(ctx.expr()))

    def visitDelete_statement(self, ctx: AhParser.Delete_statementContext):
        label = self.resolve_label(ctx.labels())
        self.delete_variable(label=label)
        self.log('Deleteing variable: ' + label)

    def visitAwait_statement(self, ctx: AhParser.Await_statementContext):
        label = self.resolve_label(ctx.labels())
        var = self.get_variable(label=label)
        if isinstance(var, GenericExecution):
            var.join()
        return var

    def visitReflection(self, ctx: AhParser.ReflectionContext) -> dict:
        label = self.resolve_label(ctx.labels())
        try:
            reflection = self.get_symbol(label=label).get_symbol_debug()
        except SymbolNotFound:
            if label in self.symbol_table.up_words:
                reflection = self.symbol_table.get_nearest_module().get_scope_debug()
            else:
                raise SymbolError
        return reflection

    def visitRequired_parameter(self, ctx: AhParser.Required_parameterContext) -> Parameter:
        label = self.resolve_label(ctx.labels())
        return Parameter(name=label, required=True)

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

    def visitAttributes(self, ctx: AhParser.AttributesContext) -> Attributes:
        attributes = Attributes()
        if ctx.SCRIPT(0):
            attributes.script = True
        if ctx.STATIC(0):
            attributes.static = True
        if ctx.ASYNC(0):
            attributes.asynchronous = True
        return attributes

    def visitAtom_string(self, ctx: AhParser.Atom_stringContext) -> str:
        line = ctx.STRING().getText()[1:-1]
        line = line.replace('\\"', '"')
        line = line.replace('\\\'', '\'')
        matches = re.findall(self.regexVar, line)
        for match in matches:
            label = match[2:-1].strip()
            label = label.replace('$', '')
            replacer = str(self.get_variable(label))
            line = line.replace(match, replacer)
            self.log('Injecting Variable into String \'' + label + '\': ' + line)
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
