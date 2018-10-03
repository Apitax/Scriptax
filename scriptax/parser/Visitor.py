from scriptax.grammar.build.Ah3Parser import Ah3Parser as AhParser, Ah3Parser
from scriptax.grammar.build.Ah3Visitor import Ah3Visitor as AhVisitorOriginal
from scriptax.parser.symbols.SymbolTable import SymbolTable, createTableFromScope
from scriptax.parser.symbols.Symbol import *
from scriptax.parser.symbols.ScriptSymbol import ScriptSymbol
from scriptax.parser.symbols.SymbolScope import SymbolScope, SCOPE_BLOCK, SCOPE_CALLBACK, SCOPE_METHOD, SCOPE_SCRIPT
from scriptax.drivers.Driver import Driver

from commandtax.models.Command import Command

from apitaxcore.models.State import State
from apitaxcore.models.Credentials import Credentials
from apitaxcore.models.Options import Options
from apitaxcore.utilities.Async import GenericExecution
from apitaxcore.utilities.Json import isJson
from apitaxcore.flow.LoadedDrivers import LoadedDrivers
from apitaxcore.flow.responses.ApitaxResponse import ApitaxResponse

import json
import re
import threading
import traceback


# TODO: SCOPE GENERATION:
#   basic symbol creators:
#     v assignment
#     sig_statement
#
#   symbol value adjusters:
#     v assignment
#
#   symbol type adjusters/verifiers:
#     v assignment
#
#   scope creators:
#     v method_statement (ADD SYMBOL TO GLOBAL SCOPE & ADD AS CHILD SCOPE OF TYPE METHOD)
#     v block            (ADD AS CHILD SCOPE OF TYPE BLOCK)
#     v callback_block   (ADD AS CHILD SCOPE OF TYPE CALLBACK)
#
#     run recursively when encountering and merge into global scope:
#       extends_statement  (MERGE SCOPES & SYMBOLS INTO GLOBAL OF SUB SCRIPT PRIOR TO CURRENT SCRIPT)
#       v import_statement   (ADD AS SCRIPT SYMBOL TYPE INTO GLOBAL SCOPE)
#
#   Scope ordering: imports, program path
#
# vTODO: Variable access in DOT notation (dict, list, symbol, straight up data)
# vTODO: Variable setting in DOT notation (dict, list, symbol, straight up data)
# vTODO: Implement class signatures using `sig`
# vTODO: Implement reflection according to GitHub issue
# TODO: Pull code out of newInstance and extends to another method
# vTODO: Support sig polymorphism for extends
# TODO: Async, Await

class AhVisitor(AhVisitorOriginal):

    def __init__(self, credentials: Credentials = None, parameters: dict = None, options: Options = None, file=None,
                 symbol_table=None):
        # Aliases
        self.log = State.log
        self.config = State.config

        # Parameters
        self.appOptions: Options = options if options is not None else Options()
        # self.appOptions.debug = True
        self.credentials: Credentials = credentials if credentials is not None else Credentials()
        self.parameters: dict = parameters if parameters is not None else {}

        # Async Threading
        self.threads = []

        # TODO: Evaluate necessity of these
        self.state = {'file': file, 'line': 0, 'char': 0}
        self.parser = None
        self.options = {}

        # Parsing status
        # Values: ok, error, exit, return
        self.status = 'ok'
        self.message = ''

        # Symbol Table
        if not symbol_table:
            self.symbol_table: SymbolTable = SymbolTable()
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

    # Helper method which executes a given scriptax string
    def parseScript(self, scriptax: str, parameters: dict = None) -> tuple:
        from scriptax.parser.utils.BoilerPlate import customizableParser
        result = customizableParser(scriptax, parameters=parameters)
        if result[1].isError():
            self.error(message=result[1].message)
            return None, None
        return result

    # Helper method which executes on a given context with a given set of symbols
    def parseScriptCustom(self, context, symbol_table: SymbolTable = None) -> tuple:
        from scriptax.parser.utils.BoilerPlate import customizableContextParser
        result = customizableContextParser(context, symbol_table=symbol_table)
        if result[1].isError():
            self.error(message=result[1].message)
            return None, None
        return result

    # Sets the current state of the parser
    def setState(self, file='', line=-1, char=-1):
        if file != '':
            self.state['file'] = file
        if line != -1:
            self.state['line'] = line
        if char != -1:
            self.state['char'] = char

    # Helper method which executes commandtax
    def executeCommand(self, command: Command) -> ApitaxResponse:
        from commandtax.flow.Connector import Connector
        if self.appOptions.debug:
            self.log.log('> Executing Commandtax: \'' + " ".join(command.command) + '\' ' + 'with parameters: ' + str(
                command.parameters))
            self.log.log('')

        if not command.credentials:
            command.credentials = self.credentials

        if not command.options:
            command.options = self.options

        connector = Connector(options=command.options, credentials=command.credentials,
                              command=" ".join(command.command), parameters=command.parameters, request=command.request)
        return connector.execute()

    # Helper method which executes a callback
    def executeCallback(self, callback=None, response: ApitaxResponse = None, result=None):
        from scriptax.parser.utils.BoilerPlate import customizableContextParser
        table = SymbolTable()
        if not result:
            result = response.getResponseBody()
        elif response:
            result = {'result': result, 'response': response}

        table.putSymbol(Symbol(name='result', symbolType=SYMBOL_VARIABLE, value=result))
        for key, value in callback['params'].items():
            table.putSymbol(Symbol(name=key, symbolType=SYMBOL_VARIABLE, value=value))
        # Returns the value found in any return statement within the callback.
        # If no return statement is in the callback this will be None
        return customizableContextParser(context=callback['block'], symbol_table=table, options=self.appOptions)[0][1]

    def setVariable(self, label, value=None, convert=True):
        return self.setSymbol(label, value=value, convert=convert)

    def setSymbol(self, label, value=None, convert=True):
        if convert:
            label = self.visit(label)
        label = label.replace('$', '')
        node, name, i = self.symbol_table.traverseToParent(label)
        components = label.split('.')[i:]

        table = createTableFromScope(node)

        # Direct referencing - ie. parent.path=, parent.parent.path=, path=
        if len(components) == 1:
            table.putSymbol(Symbol(name=components[0], symbolType=SYMBOL_VARIABLE, value=value))
            return True

        symbol, i = table.getSymbolWithLength(components[0], symbolType=SYMBOL_VARIABLE)

        if symbol:
            i += 1

        # components will be at least 2
        # use cases:
        # 1. instance navigation via composition:
        #   parent.someInstance.someInstanceOnThatOne.path=  (len=3), someInstance.path=  (len=2)
        # 2. instance setting:  someInstance = new Instance();
        try:
            while len(components) > i + 1:
                if symbol.dataType == DATA_INSTANCE:
                    table = createTableFromScope(symbol.value)
                    symbol, j = table.getSymbolWithLength(name=components[i], symbolType=SYMBOL_VARIABLE)
                elif symbol.dataType == DATA_DICT:
                    symbol = symbol.value[str(components[i])]
                    if not isinstance(symbol, Symbol):
                        symbol = Symbol(symbolType=SYMBOL_VARIABLE, value=symbol)
                elif symbol.dataType == DATA_LIST:
                    symbol = symbol.value[int(components[i])]
                    if not isinstance(symbol, Symbol):
                        symbol = Symbol(symbolType=SYMBOL_VARIABLE, value=symbol)
                elif symbol.dataType == DATA_THREAD:
                    return False
                elif symbol.dataType == DATA_PYTHONIC:
                    return False
                else:
                    # print(symbol.dataType)
                    self.error(message="Symbol `" + label + "` is corrupt and not settable.")
                    return False
                i += 1

            final = components.pop()
            if symbol.dataType == DATA_INSTANCE:
                table = createTableFromScope(symbol.value)
                table.putSymbol(Symbol(name=final, symbolType=SYMBOL_VARIABLE, value=value))
            elif symbol.dataType == DATA_DICT:
                symbol.value[str(final)] = value
            elif symbol.dataType == DATA_LIST:
                symbol.value[int(final)] = value
            else:
                table.putSymbol(Symbol(name=final, symbolType=SYMBOL_VARIABLE, value=value))
            return True
        except:
            print("Exception during variable setting")
            traceback.print_exc()
            self.error(message="Symbol `" + label + "` is corrupt and not settable.")
            return False

    def getVariable(self, label=None, convert=True):
        # return self.getSymbol(label=label, convert=convert).value
        if convert:
            label = self.visit(label)
        try:
            return self.getSymbol(label, False).value
        except:
            self.error(message="Symbol `" + label + "` not found in scope `" + self.symbol_table.current.name + "`")
            return None

    def getSymbol(self, label, convert=True, symbolType=SYMBOL_VARIABLE):

        if convert:
            label = self.visit(label)
        label = label.replace('$', '')
        node, name, i = self.symbol_table.traverseToParent(label)
        components = label.split('.')[i:]

        table = createTableFromScope(node)

        if len(components) == 1:
            symbol, i = table.getSymbolWithLength(components[0], symbolType=symbolType)
            return symbol

        symbol, i = table.getSymbolWithLength(components[0], symbolType=SYMBOL_VARIABLE)
        if not symbol:
            symbol, i = table.getSymbolWithLength(components[0], symbolType=SYMBOL_SCRIPT)

        if symbol:
            i += 1

        try:
            while len(components) > i:
                if len(components) > i + 1:
                    type = SYMBOL_VARIABLE
                else:
                    type = symbolType
                if symbol.dataType == DATA_INSTANCE:
                    table = createTableFromScope(symbol.value)
                    symbol, j = table.getSymbolWithLength(name=components[i], symbolType=type)
                elif symbol.dataType == DATA_DICT:
                    symbol = symbol.value[str(components[i])]
                    if not isinstance(symbol, Symbol):
                        symbol = Symbol(symbolType=type, value=symbol)
                elif symbol.dataType == DATA_LIST:
                    symbol = symbol.value[int(components[i])]
                    if not isinstance(symbol, Symbol):
                        symbol = Symbol(symbolType=type, value=symbol)
                elif symbol.dataType == DATA_THREAD:
                    return None
                elif symbol.dataType == DATA_PYTHONIC:
                    return None
                i += 1

            return symbol

        except:
            print("Exception during variable fetching")
            traceback.print_exc()
            self.error(message="Symbol `" + label + "` not found in scope.")
            return None

    def deleteVariable(self, label, convert=True):
        return self.deleteSymbol(label, convert=convert)

    def deleteSymbol(self, label, convert=True, symbolType=SYMBOL_VARIABLE):
        if convert:
            label = self.visit(label)
        label = label.replace('$', '')
        node, name, i = self.symbol_table.traverseToParent(label)
        components = label.split('.')[i:]

        table = createTableFromScope(node)

        # Direct referencing - ie. parent.path=, parent.parent.path=, path=
        if len(components) == 1:
            table.deleteSymbol(name=components[0], symbolType=SYMBOL_VARIABLE)
            return True

        symbol, i = table.getSymbolWithLength(components[0], symbolType=SYMBOL_VARIABLE)

        if symbol:
            i += 1

        # components will be at least 2
        # use cases:
        # 1. instance navigation via composition:
        #   parent.someInstance.someInstanceOnThatOne.path=  (len=3), someInstance.path=  (len=2)
        # 2. instance setting:  someInstance = new Instance();
        try:
            while len(components) > i + 1:
                if symbol.dataType == DATA_INSTANCE:
                    table = createTableFromScope(symbol.value)
                    symbol, j = table.getSymbolWithLength(name=components[i], symbolType=SYMBOL_VARIABLE)
                elif symbol.dataType == DATA_DICT:
                    symbol = symbol.value[str(components[i])]
                    if not isinstance(symbol, Symbol):
                        symbol = Symbol(symbolType=SYMBOL_VARIABLE, value=symbol)
                elif symbol.dataType == DATA_LIST:
                    symbol = symbol.value[int(components[i])]
                    if not isinstance(symbol, Symbol):
                        symbol = Symbol(symbolType=SYMBOL_VARIABLE, value=symbol)
                elif symbol.dataType == DATA_THREAD:
                    return False
                elif symbol.dataType == DATA_PYTHONIC:
                    return False
                else:
                    # print(symbol.dataType)
                    self.error(message="Symbol `" + label + "` is corrupt and not settable.")
                    return False
                i += 1

            final = components.pop()
            if symbol.dataType == DATA_INSTANCE:
                table = createTableFromScope(symbol.value)
                table.deleteSymbol(name=final, symbolType=SYMBOL_VARIABLE)
            elif symbol.dataType == DATA_DICT:
                symbol.value.pop(str(final))
            elif symbol.dataType == DATA_LIST:
                del symbol.value[int(final)]
            else:
                table.deleteSymbol(name=final, symbolType=SYMBOL_VARIABLE)
            return True
        except:
            print("Exception during variable setting")
            traceback.print_exc()
            self.error(message="Symbol `" + label + "` is corrupt and not settable.")
            return False

    # Dynamic mustache syntax injection
    def inject(self, line):
        matches = re.findall(self.regexVar, line)
        for match in matches:
            label = match[2:-2].strip()
            replacer = self.getVariable(label, convert=False)
            line = line.replace(match, replacer)
        return line

    # Visit a parse tree produced by AhParser#prog.
    # TODO: Improve error message format
    def visitProg(self, ctx: AhParser.ProgContext):
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

    # Visit a parse tree produced by Ah3Parser#script_structure.
    def visitScript_structure(self, ctx: AhParser.Script_structureContext):
        self.visit(ctx.global_statements())
        self.visit(ctx.root_level_statements())
        return self.visit(ctx.statements())

    # Visit a parse tree produced by Ah3Parser#global_statements.
    def visitGlobal_statements(self, ctx: AhParser.Global_statementsContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by Ah3Parser#root_level_statements.
    def visitRoot_level_statements(self, ctx: AhParser.Root_level_statementsContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by AhParser#statements.
    def visitStatements(self, ctx: AhParser.StatementsContext) -> tuple:
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
    def visitStatement(self, ctx: AhParser.StatementContext) -> tuple:
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

        self.setState(line=ctx.start.line)  # TODO: Try to add character here as well

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

    # Visit a parse tree produced by AhParser#set_var.
    def visitAssignment(self, ctx: AhParser.AssignmentContext):
        label = self.visit(ctx.labels())
        value = None

        if ctx.expr():
            value = self.visit(ctx.expr())

        if not ctx.EQUAL():
            var = self.getVariable(label=label, convert=False)
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
            var = self.getVariable(label=label, convert=False)
            if not isinstance(var, list):
                self.error("Appending to a list requires the variable being a list")
                return
            var.append(value)
            tval = value
            value = var
            self.setVariable(label=label, value=value, convert=False)
            if isinstance(tval, threading.Thread):
                tval.label = label + "." + str(len(value) - 1)
                tval.start()
        else:
            self.setVariable(label=label, value=value, convert=False)
            if isinstance(value, threading.Thread):
                value.label = label
                value.start()

        if self.appOptions.debug:
            self.log.log('> Assigning Variable: ' + label + ' = ' + str(
                value))
            self.log.log('')

    # Visit a parse tree produced by AhParser#flow.
    def visitFlow(self, ctx: AhParser.FlowContext) -> tuple:
        if ctx.if_statement():
            return self.visit(ctx.if_statement())
        if ctx.while_statement():
            return self.visit(ctx.while_statement())
        if ctx.for_statement():
            return self.visit(ctx.for_statement())

    # Visit a parse tree produced by Ah3Parser#create_instance.
    def visitCreate_instance(self, ctx: AhParser.Create_instanceContext):
        label = self.visit(ctx.label())
        symbol: ScriptSymbol = self.symbol_table.getSymbol(name=label, symbolType=SYMBOL_SCRIPT)
        scriptax = symbol.driver.getDriverScript(symbol.path)
        parameters = self.visit(ctx.optional_parameters_block())
        parser = self.parseScript(scriptax, parameters=parameters)[1]
        instanceTable: SymbolTable = parser.symbol_table
        instanceTable.resetTable()
        instanceTable.enterScope()  # SymbolTable()
        instanceScope = instanceTable.current
        instanceScope.setMeta(name=label, scopeType=SCOPE_SCRIPT)
        return instanceScope

    # Visit a parse tree produced by Ah3Parser#method_statement.
    def visitMethod_statement(self, ctx: AhParser.Method_statementContext):
        self.symbol_table.current.addSymbol(
            symbol=Symbol(name=self.visit(ctx.label()), symbolType=SYMBOL_METHOD, dataType=DATA_CONTEXT,
                          value=ctx))
        # return self.visitChildren(ctx)

    # Visit a parse tree produced by Ah3Parser#method_call.
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
                self.executeCallback(callback=callback, result=item)
        else:
            self.error("An each loop must be passed a list")

    # Visit a parse tree produced by AhParser#condition.
    def visitCondition(self, ctx: AhParser.ConditionContext):
        condition = self.visit(ctx.expr())

        if self.appOptions.debug:
            self.log.log('>> Evaluated Flow Condition as: ' + str(condition))
            self.log.log('')

        return condition

    # Visit a parse tree produced by AhParser#block.
    def visitBlock(self, ctx: AhParser.BlockContext) -> tuple:
        self.symbol_table.enterScope()
        self.symbol_table.current.setMeta(scopeType=SCOPE_BLOCK)
        result = False, None
        if ctx.statements():
            result = self.visit(ctx.statements())
        else:
            result = self.visit(ctx.statement())
        self.symbol_table.exitScope()
        return result

    # Visit a parse tree produced by AhParser#callback.
    def visitCallback(self, ctx: AhParser.CallbackContext):
        parameters = {}
        if ctx.optional_parameters_block():
            parameters = self.visit(ctx.optional_parameters_block())
        return {"params": parameters, "block": ctx.callback_block()}

    # Visit a parse tree produced by AhParser#callback_block.
    def visitCallback_block(self, ctx: AhParser.Callback_blockContext):
        return self.visit(ctx.statements())

    # Visit a parse tree produced by AhParser#optional_parameters_block.
    def visitOptional_parameters_block(self, ctx: AhParser.Optional_parameters_blockContext) -> dict:
        i = 0
        parameters = {}
        while ctx.optional_parameter(i):
            opParam = self.visit(ctx.optional_parameter(i))
            parameters[opParam['label']] = opParam['value']
            i += 1
        return parameters

    # Visit a parse tree produced by Ah3Parser#sig_parameter_block.
    def visitSig_parameter_block(self, ctx: AhParser.Sig_parameter_blockContext) -> list:
        i = 0
        parameters = []
        while ctx.sig_parameter(i):
            opParam = self.visit(ctx.sig_parameter(i))
            param = {"label": opParam['label']}
            if 'value' in opParam:
                param['value'] = opParam['value']
            parameters.append(param)
            i += 1
        return parameters

    # Visit a parse tree produced by AhParser#sig_parameter.
    def visitSig_parameter(self, ctx: AhParser.Sig_parameterContext):
        if ctx.labels():
            return {"label": self.visit(ctx.labels())}
        else:
            return self.visit(ctx.optional_parameter())

    # Visit a parse tree produced by AhParser#call_parameter.
    def visitCall_parameter(self, ctx: AhParser.Call_parameterContext):
        if ctx.expr():
            return {"value": self.visit(ctx.expr())}
        else:
            return self.visit(ctx.optional_parameter())

    # Visit a parse tree produced by AhParser#optional_parameter.
    def visitOptional_parameter(self, ctx: AhParser.Optional_parameterContext):
        return {"label": self.visit(ctx.labels()), "value": self.visit(ctx.expr())}

    # Visit a parse tree produced by AhParser#commandtax.
    def visitCommandtax(self, ctx: AhParser.CommandtaxContext):
        firstArg = self.visit(ctx.expr())
        command = ""
        strict = True
        credentials = None

        if not ctx.COMMANDTAX():
            command += "api"
            if ctx.GET():
                command += " --get"
            if ctx.POST():
                command += " --post"
            if ctx.PUT():
                command += " --put"
            if ctx.PATCH():
                command += " --patch"
            if ctx.DELETE():
                command += " --delete"
            command += " --url " + firstArg

        elif ctx.COMMANDTAX():
            command = firstArg

        if ctx.atom_obj_dict():
            dataArg = self.visit(ctx.atom_obj_dict())
            if 'post' in dataArg:
                command += " --data-post '" + json.dumps(dataArg['post']) + "'"
            if 'query' in dataArg:
                command += " --data-query '" + json.dumps(dataArg['query']) + "'"
            if 'path' in dataArg:
                command += " --data-path '" + json.dumps(dataArg['path']) + "'"
            if 'header' in dataArg:
                command += " --data-header '" + json.dumps(dataArg['header']) + "'"
            if 'driver' in dataArg:
                command += " --apitax-driver " + dataArg['driver']
            if 'strict' in dataArg:
                strict = bool(dataArg['strict'])
            if 'auth' in dataArg:
                credentials = dataArg['auth']

        parameters = {}
        if ctx.optional_parameters_block():
            parameters = self.visit(ctx.optional_parameters_block())

        return {'command': command, 'parameters': parameters, 'strict': strict, 'credentials': credentials}

    # Visit a parse tree produced by AhParser#execute.
    def visitExecute(self, ctx):
        resolvedCommand = self.visit(ctx.commandtax())
        strict = resolvedCommand['strict']

        command = Command(command=resolvedCommand['command'], parameters=resolvedCommand['parameters'],
                          credentials=resolvedCommand['credentials'])

        response: ApitaxResponse = self.executeCommand(command)

        if strict and not response.isStatusSuccess():
            self.error('Request returned non-success status code while in strict mode. Request returned: Status ' +
                       str(
                           response.getResponseStatusCode()) + ' ' + str(response.getResponseBody()))
            return None

        result = response.getResponseBody()

        if ctx.callback():
            callback = self.visit(ctx.callback())
            result = self.executeCallback(callback=callback, response=response)

        return dict({"command": command, "commandHandler": response, "result": result})

    # Visit a parse tree produced by AhParser#async_execute.
    def visitAsync_execute(self, ctx: AhParser.Async_executeContext):
        resolvedCommand = self.visit(ctx.commandtax())
        if ctx.callback():
            resolvedCommand['callback'] = self.visit(ctx.callback())
        thread = GenericExecution(self, "Async execution and callback", resolvedCommand, log=self.log,
                                  debug=self.appOptions.debug, sensitive=self.appOptions.sensitive)
        self.threads.append(thread)
        return thread

    # Visit a parse tree produced by AhParser#await.
    def await_statement(self):
        if not ctx.labels():
            for thread in self.threads:
                thread.join()
            return
        threads = self.getVariable(ctx.labels())
        if isinstance(threads, list):
            for thread in threads:
                if isinstance(thread, threading.Thread):
                    thread.join()
        elif isinstance(threads, threading.Thread):
            threads.join()

    # Visit a parse tree produced by AhParser#labels.
    def visitLabels(self, ctx: AhParser.LabelsContext):

        label = [self.visit(ctx.label_comp(0))]
        i = 0
        while ctx.DOT(i):
            label.append(str(self.visit(ctx.label_comp(i + 1))))
            i += 1

        label = '.'.join(label)

        return label.replace('$', '')

    # Visit a parse tree produced by AhParser#label_comp.
    def visitLabel_comp(self, ctx: AhParser.Label_compContext):
        if ctx.label():
            return self.visit(ctx.label())
        else:
            return self.visit(ctx.inject())

    # Visit a parse tree produced by Ah3Parser#label.
    def visitLabel(self, ctx: AhParser.LabelContext):
        return ctx.LABEL().getText()

    # Visit a parse tree produced by Ah3Parser#attribute.
    def visitAttribute(self, ctx: AhParser.AttributeContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by Ah3Parser#extends_statement.
    def visitExtends_statement(self, ctx: AhParser.Extends_statementContext):
        label = self.visit(ctx.label())
        symbol: ScriptSymbol = self.symbol_table.getSymbol(name=label, symbolType=SYMBOL_SCRIPT)
        scriptax = symbol.driver.getDriverScript(symbol.path)
        parameters = {'import': None}
        if ctx.optional_parameters_block():
            parameters = self.visit(ctx.optional_parameters_block())
        parser = self.parseScript(scriptax, parameters=parameters)[1]

        extendsTable: SymbolTable = parser.symbol_table
        extendsTable.resetTable()
        extendsTable.enterScope()
        extendsScope: SymbolScope = extendsTable.current
        extendsScope.setMeta(name=label, scopeType=SCOPE_SCRIPT)

        # print(extendsTable.printTable())

        # for sym in extendsScope.symbols:

        current = self.symbol_table.current
        self.symbol_table.exitScopeAndDelete()
        self.symbol_table.insertScope(scope=extendsScope)
        self.symbol_table.insertScope(scope=current)
        # print(self.symbol_table.printTable())

    # Visit a parse tree produced by AhParser#params_statement.
    def visitSig_statement(self, ctx: AhParser.Sig_statementContext):
        specialOp = False  # Helps with import and extends
        if self.parameters and len(self.parameters) == 1 and 'import' in self.parameters and self.parameters[
            'import'] is None:
            specialOp = True

        parameters = self.visit(ctx.sig_parameter_block())
        for param in parameters:
            label = param['label']

            if specialOp:
                if 'value' in param:
                    value = param['value']
                else:
                    value = None
            else:
                if label in self.parameters:
                    value = self.parameters[label]
                elif 'value' in param:
                    value = param['value']
                else:
                    self.error(
                        'Insufficient parameters. Expected Parameter: \'' + str(label) + '\'')
                    return None

            self.setVariable(label=label, value=value, convert=False)

    # Visit a parse tree produced by AhParser#options_statement.
    def visitOptions_statement(self, ctx: AhParser.Options_statementContext):
        # name -> str
        # help -> str
        # summary -> str
        # description -> str
        # author -> str
        # version -> str
        # link -> str
        # available -> bool
        # enabled -> bool
        # access -> list['apitax', 'roles']
        self.options = self.visit(ctx.optional_parameters_block())

    # Visit a parse tree produced by AhParser#delete_statement.
    def visitDelete_statement(self, ctx: AhParser.Delete_statementContext):
        label = self.visit(ctx.labels())
        self.deleteVariable(label=label, convert=False)
        if self.appOptions.debug:
            self.log.log('> Deleteing variable: ' + label)
            self.log.log('')

    # Visit a parse tree produced by AhParser#error_statement.
    def visitError_statement(self, ctx: AhParser.Error_statementContext):
        message = "No error message was specified"
        if ctx.expr():
            message = self.visit(ctx.expr())
        self.error(message)

    # Visit a parse tree produced by AhParser#return_statement.
    def visitReturn_statement(self, ctx: AhParser.Return_statementContext):
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

    # Visit a parse tree produced by Ah3Parser#auth_statement.
    def visitAuth_statement(self, ctx: Ah3Parser.Auth_statementContext):
        parameters = self.visit(ctx.optional_parameters_block())

        extra = {}
        username = None
        password = None
        token = None

        if 'extra' in parameters:
            extra = parameters['extra']

        if 'username' in parameters:
            username = parameters['username']

        if 'password' in parameters:
            password = parameters['password']

        if 'token' in parameters:
            token = parameters['token']

        credentials = Credentials(username=username, password=password, token=token, extra=extra)

        return credentials

    # Visit a parse tree produced by AhParser#endpoint_statement.
    def visitEndpoint_statement(self, ctx: AhParser.Endpoint_statementContext):
        name = self.visit(ctx.expr())
        try:
            name.find('@')
            name = name.split('@')
            driver = LoadedDrivers.getDriver(name[1])
            name = name[0]
        except:
            if self.appOptions.driver:
                driver = LoadedDrivers.getDriver(self.appOptions.driver)
            else:
                driver = LoadedDrivers.getDefaultDriver()
        endpoints = driver.getEndpointCatalog()['endpoints']
        if name in endpoints:
            return endpoints[name]['value']
        else:
            self.error("The endpoint requested does not exist")
            return None

    # Visit a parse tree produced by Ah3Parser#import_statement.
    def visitImport_statement(self, ctx: AhParser.Import_statementContext):
        driver: Driver = LoadedDrivers.getPrimaryDriver()
        labelIndex = 0
        if ctx.FROM():
            driver = self.visit(ctx.label(labelIndex))
            driver = LoadedDrivers.getDriver(driver)
            labelIndex += 1

        path = self.visit(ctx.labels())

        name = None
        if ctx.AS():
            name = self.visit(ctx.label(labelIndex))
        else:
            name = path.split('.')[-1]

        path = path.replace('.', '/') + '.ah'

        scriptax = driver.getDriverScript(path)

        parameters = {'import': None}
        if ctx.optional_parameters_block():
            parameters = self.visit(ctx.optional_parameters_block())
        parser = self.parseScript(scriptax, parameters=parameters)[1]

        importTable: SymbolTable = parser.symbol_table
        importTable.resetTable()
        importTable.enterScope()  # SymbolTable()
        importScope = importTable.current
        importScope.setMeta(name=name, scopeType=SCOPE_SCRIPT)

        # Insert the script scope into our scope and add a symbol to reference it
        reference = self.symbol_table.current.parent.insertScope(importScope)
        # self.symbol_table.exitScope()
        self.symbol_table.current.addSymbol(
            symbol=ScriptSymbol(name=name, symbolType=SYMBOL_SCRIPT, dataType=DATA_SCRIPT, value=reference, path=path,
                                driver=driver))
        # return self.visitChildren(ctx)

    # Visit a parse tree produced by AhParser#casting.
    def visitCasting(self, ctx: AhParser.CastingContext):
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

    # Visit a parse tree produced by AhParser#log.
    def visitLog(self, ctx: AhParser.LogContext):
        if ctx.expr():
            self.log.log('> Logging: ' + json.dumps(self.visit(ctx.expr())))
            self.log.log('')

    # Visit a parse tree produced by AhParser#count.
    def visitCount(self, ctx: AhParser.CountContext):
        return len(self.visit(ctx.expr()))

    # Visit a parse tree produced by Ah3Parser#reflection.
    def visitReflection(self, ctx: AhParser.ReflectionContext):
        symbol = self.getSymbol(label=ctx.labels())
        return symbol.getSymbolDebug()

    # Visit a parse tree produced by AhParser#inject.
    def visitInject(self, ctx: AhParser.InjectContext):
        returner = self.visit(ctx.expr())
        if self.appOptions.debug:
            self.log.log('> Injecting into: ' + ctx.getText() + ' with the value ' + str(returner))
            self.log.log('')
        return returner

    # Visit a parse tree produced by AhParser#atom.
    def visitAtom(self, ctx: AhParser.AtomContext):

        if ctx.atom_obj_dict():
            return self.visit(ctx.atom_obj_dict())

        if ctx.atom_obj_list():
            return self.visit(ctx.atom_obj_list())

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

    # Visit a parse tree produced by AhParser#obj_dict.
    def visitAtom_obj_dict(self, ctx: AhParser.Atom_obj_dictContext):
        dictionary = {}
        i = 0
        if ctx.COLON(0):
            dictionary[self.visit(ctx.expr(0))] = self.visit(ctx.expr(1))
        while ctx.COMMA(i) and ctx.expr((i + 1) * 2):
            base = (i + 1) * 2
            dictionary[self.visit(ctx.expr(base))] = self.visit(ctx.expr(base + 1))
            i += 1
        return dictionary

    # Visit a parse tree produced by AhParser#obj_list.
    def visitAtom_obj_list(self, ctx: AhParser.Atom_obj_listContext):
        parameters = []
        i = 0
        if ctx.expr(0):
            parameters.append(self.visit(ctx.expr(0)))
        while ctx.COMMA(i) and ctx.expr(i + 1):
            parameters.append(self.visit(ctx.expr(i + 1)))
            i += 1
        return parameters

    # Visit a parse tree produced by AhParser#string.
    def visitAtom_string(self, ctx: AhParser.Atom_stringContext):
        line = ctx.STRING().getText()[1:-1]
        line = line.replace('\\"', '"')
        line = line.replace('\\\'', '\'')
        matches = re.findall(self.regexVar, line)
        for match in matches:
            label = match[2:-2].strip()
            label = label.replace('$', '')
            replacer = str(self.getVariable(label, convert=False))
            line = line.replace(match, replacer)
            if self.appOptions.debug:
                self.log.log('> Injecting Variable into String \'' + label + '\': ' + line)
                self.log.log('')
        return line

    # Visit a parse tree produced by AhParser#number.
    def visitAtom_number(self, ctx: AhParser.Atom_numberContext):
        if ctx.INT():
            return int(ctx.INT().getText())
        else:
            return float(ctx.FLOAT().getText())

    # Visit a parse tree produced by AhParser#boolean.
    def visitAtom_boolean(self, ctx: AhParser.Atom_booleanContext):
        if ctx.TRUE():
            return True
        if ctx.FALSE():
            return False

    # Visit a parse tree produced by Ah3Parser#atom_hex.
    def visitAtom_hex(self, ctx: AhParser.Atom_hexContext):
        return '0x' + str(ctx.HEX().getText())[2:].upper()

    # Visit a parse tree produced by Ah3Parser#atom_none.
    def visitAtom_none(self, ctx: AhParser.Atom_noneContext):
        return None
