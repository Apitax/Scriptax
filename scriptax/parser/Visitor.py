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

import json
import re
import threading


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
#       import_statement   (ADD AS SCRIPT SYMBOL TYPE INTO GLOBAL SCOPE)
#
#   Scope ordering: imports, program path
#
# TODO: METHOD CALLS:
#  Because the symbol table contains all the relevant data, all that must be saved is the method block context.
#  As long as we ensure the correct scope is set when we visit that block context, everything **SHOULD** work fine

class AhVisitor(AhVisitorOriginal):

    def __init__(self, credentials: Credentials = Credentials(), parameters={}, options: Options = Options(), file='',
                 symbol_table=None):
        # Aliases
        self.log = State.log
        self.config = State.config

        # Parameters
        self.appOptions = options
        #self.appOptions.debug = True
        self.credentials = credentials
        self.parameters = parameters

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
            self.symbol_table = SymbolTable()
        else:
            self.symbol_table = symbol_table

        # Used for mustache syntax dynamic replacement
        self.regexVar = '{{[ ]{0,}[A-z0-9_$.\-]{1,}[ ]{0,}}}'

    def parseScript(self, scriptax: str):
        from scriptax.parser.utils.BoilerPlate import standardParser
        return standardParser(scriptax)

    def parseScriptCustom(self, context, symbol_table: SymbolTable = None):
        from scriptax.parser.utils.BoilerPlate import customizableContextParser
        return customizableContextParser(context, symbol_table=symbol_table)

    def setState(self, file='', line=-1, char=-1):
        if (file != ''):
            self.state['file'] = file
        if (line != -1):
            self.state['line'] = line
        if (char != -1):
            self.state['char'] = char

    # TODO: Redo, this is garbage
    def executeCommand(self, command: Command):
        from apitaxcore.flow.Connector import Connector
        if (self.appOptions.debug):
            self.log.log('> Executing Commandtax: \'' + resolvedCommand['command'] + '\' ' + 'with parameters: ' + str(
                resolvedCommand['parameters']), logPrefix)
            self.log.log('')

        credentials = None
        if (resolvedCommand['auth']):
            credentials = Credentials(username=resolvedCommand['auth'].username, password=resolvedCommand.password,
                                      token=resolvedCommand.token)
        else:
            credentials = self.credentials

        connector = Connector(options=Options(debug=self.appOptions.debug, sensitive=self.appOptions.sensitive,
                                              driver=resolvedCommand['driver']),
                              credentials=credentials,
                              command=resolvedCommand['command'], parameters=resolvedCommand['parameters'])
        commandHandler = connector.execute()

        if (hasattr(commandHandler.getRequest(), 'parser')):
            if (commandHandler.getRequest().parser.isError()):
                self.error('Subscript contains error: ' + commandHandler.getRequest().parser.isError()['message'],
                           logPrefix)

        if (resolvedCommand['strict'] and commandHandler.getRequest().getResponseStatusCode() >= 300):
            self.error('Request returned non-success status code while in strict mode. Request returned: Status ' +
                       str(
                           commandHandler.getRequest().getResponseStatusCode()) + ' ' + commandHandler.getRequest().getResponseBody(),
                       logPrefix)

        returnResult = commandHandler.getReturnedData()
        if ('callback' in resolvedCommand):
            returnResult = self.executeIsolatedCallback(resolvedCommand['callback'], returnResult, logPrefix)

        return dict({"command": resolvedCommand['command'], "commandHandler": commandHandler, "result": returnResult})

    def getVariable(self, label, convert=True):
        if (convert):
            label = self.visit(label)
        try:
            return self.symbol_table.getSymbol(name=label, symbolType=SYMBOL_VARIABLE).value
        except:
            self.error(message="Symbol `" + label + "` not found in scope `" + self.symbol_table.current.name + "`")
            return None

    # TODO: Repurpose to utilize symbol table
    def getSymbol(self, label, convert=True):
        if convert:
            label = self.visit(label)
        try:
            return self.symbol_table.getSymbol(name=label, symbolType=SYMBOL_VARIABLE)
        except:
            self.error(message="Symbol `" + label + "` not found in scope `" + self.symbol_table.current.name + "`")
            return None

    # TODO: WTF?
    def useOptions(self):
        if (self.options['params']):

            if (len(self.options['params']) != len(self.data.getVar('params.passed'))):
                self.error(
                    'Insufficient parameters. Expected: ' + str(self.options['params']) + ' but received: ' + str(
                        self.data.getVar('params.passed')))
            else:
                i = 0
                for param in self.options['params']:
                    self.data.storeVar('params.' + param, self.data.getVar('params.passed.' + param))
                    i += 1

    # Dynamic mustache syntax injection
    def inject(self, line):
        matches = re.findall(self.regexVar, line)
        for match in matches:
            label = match[2:-2].strip()
            replacer = self.getVariable(label, convert=False)
            line = line.replace(match, replacer)
        return line

    # TODO: Repurpose to use symbol table
    # TODO: Repurpose to execute a block context generically
    def executeCallback(self, callback, resultScope, logPrefix=''):
        visitor = AhVisitor(options=Options(debug=self.appOptions.debug, sensitive=self.appOptions.sensitive))
        visitor.setState(file=self.state['file'])
        visitor.log.prefix = logPrefix
        visitor.data.storeVar('result', resultScope)
        for key, value in callback['params'].items():
            visitor.data.storeVar(key, value)
        block = callback['block']
        callbackResult = visitor.visit(block)
        return visitor.data.getVar('result')

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

    # Visit a parse tree produced by AhParser#prog.
    # TODO: Improve error message format
    def visitProg(self, ctx: AhParser.ProgContext):
        self.symbol_table.enterScope()
        self.symbol_table.current.setMeta(scopeType=SCOPE_SCRIPT)
        self.parser = ctx.parser
        temp = self.visitChildren(ctx)

        if (self.isError()):
            error = self.isError()
            self.log.error(
                self.message + ' in ' + str(self.state['file']) + ' @' + str(self.state['line']) + ':' + str(
                    self.state['char']))
            if (self.appOptions.debug):
                self.log.log('')
                self.log.log('')
        self.symbol_table.exitScope()
        return self

    # Visit a parse tree produced by Ah3Parser#script_structure.
    def visitScript_structure(self, ctx: AhParser.Script_structureContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by Ah3Parser#global_statements.
    def visitGlobal_statements(self, ctx: AhParser.Global_statementsContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by Ah3Parser#root_level_statements.
    def visitRoot_level_statements(self, ctx: AhParser.Root_level_statementsContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by AhParser#statements.
    def visitStatements(self, ctx: AhParser.StatementsContext):
        if (self.isReturn() or self.isError()):
            return
        temp = self.visitChildren(ctx)
        return temp

    # Visit a parse tree produced by AhParser#statement.
    def visitStatement(self, ctx: AhParser.StatementContext):
        if (self.isReturn()):
            return

        if (self.isError()):
            return

        debugTemp = self.appOptions.debug
        sensitiveTemp = self.appOptions.sensitive

        line = ctx.getText().strip()
        if (line != "" and self.appOptions.debug):
            if (ctx.NOT()):
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

        temp = self.visitChildren(ctx)

        if (line != "" and self.appOptions.debug):
            self.log.log('')

        self.setState(line=ctx.start.line)  # TODO: Try to add character here as well

        if (ctx.NOT() and line != "" and debugTemp):
            self.log.log('> Setting debug and sensitive back to their original values')
            self.log.log('')
            self.log.log('')
            self.appOptions.debug = debugTemp
            self.appOptions.sensitive = sensitiveTemp

        return temp

    # Visit a parse tree produced by AhParser#terminated.
    def visitTerminated(self, ctx: AhParser.TerminatedContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by AhParser#non_terminated.
    def visitNon_terminated(self, ctx: AhParser.Non_terminatedContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by AhParser#executers.
    def visitExecute_statement(self, ctx: AhParser.Execute_statementContext):
        if (ctx.execute()):
            return self.visit(ctx.execute())
        if (ctx.async_execute()):
            thread = self.visit(ctx.async_execute())
            thread.start()
            return thread

    # Visit a parse tree produced by AhParser#expr.
    # TODO: add support for method, instance, reflection etc.
    def visitExpr(self, ctx):  # Get number of terms and loop this code for #terms - 1

        if (ctx.reflection()):
            return self.visit(ctx.reflection())

        if (ctx.create_instance()):
            return self.visit(ctx.create_instance())

        if (ctx.method_call()):
            return self.visit(ctx.method_call())

        if (ctx.execute()):
            return self.visit(ctx.execute())['result']

        if (ctx.async_execute()):
            return self.visit(ctx.async_execute())

        if (ctx.atom()):
            return self.visit(ctx.atom())

        if (ctx.casting()):
            return self.visit(ctx.casting())

        if (ctx.login_statement()):
            return self.visit(ctx.login_statement())

        if (ctx.endpoint_statement()):
            return self.visit(ctx.endpoint_statement())

        if (ctx.count()):
            return self.visit(ctx.count())

        if (ctx.labels()):
            return self.getVariable(ctx.labels())  # TODO: Remove isRequest from here as it is no longer a thing

        if (ctx.inject()):
            return self.visit(ctx.inject())

        if (ctx.MINUS() and not ctx.expr(1)):
            return self.visit(ctx.expr(0)) * -1

        if (ctx.NOT()):
            return not self.visit(ctx.expr(0))

        if (ctx.AND()):
            return self.visit(ctx.expr(0)) and self.visit(ctx.expr(1))

        if (ctx.OR()):
            return self.visit(ctx.expr(0)) or self.visit(ctx.expr(1))

        if (ctx.EQ()):
            return self.visit(ctx.expr(0)) == self.visit(ctx.expr(1))

        if (ctx.NEQ()):
            return self.visit(ctx.expr(0)) != self.visit(ctx.expr(1))

        if (ctx.GE()):
            return self.visit(ctx.expr(0)) >= self.visit(ctx.expr(1))

        if (ctx.LE()):
            return self.visit(ctx.expr(0)) <= self.visit(ctx.expr(1))

        if (ctx.GT()):
            return self.visit(ctx.expr(0)) > self.visit(ctx.expr(1))

        if (ctx.LT()):
            return self.visit(ctx.expr(0)) < self.visit(ctx.expr(1))

        if (ctx.LPAREN()):
            return self.visit(ctx.expr(0))

        if (ctx.POW()):
            return self.visit(ctx.expr(0)) ** self.visit(ctx.expr(1))

        if (ctx.PLUS()):
            left = self.visit(ctx.expr(0))
            right = self.visit(ctx.expr(1))
            if ((isinstance(left, str) and not isinstance(right, str)) or (
                    isinstance(right, str) and not isinstance(left, str))):
                left = str(left)
                right = str(right)
                if (self.appOptions.debug):
                    self.log.log('> Implicit cast to string: \'' + left + '\' + \'' + right + '\'')
                    self.log.log('')
            return left + right

        if (ctx.MINUS()):
            return self.visit(ctx.expr(0)) - self.visit(ctx.expr(1))

        if (ctx.MUL()):
            return self.visit(ctx.expr(0)) * self.visit(ctx.expr(1))

        if (ctx.DIV()):
            return self.visit(ctx.expr(0)) / self.visit(ctx.expr(1))

        return self.visitChildren(ctx)

    # Visit a parse tree produced by AhParser#set_var.
    def visitAssignment(self, ctx: AhParser.AssignmentContext):
        label = self.visit(ctx.labels())
        value = None

        if (ctx.expr()):
            value = self.visit(ctx.expr())

        if (not ctx.EQUAL()):
            # TODO: Double check that this still works
            var = self.symbol_table.getSymbol(name=label)
            # var = self.data.getVar(label)
            if (ctx.D_PLUS()):
                value = var + 1
            elif (ctx.D_MINUS()):
                value = var - 1
            else:
                if (ctx.PE()):
                    value = var + value
                elif (ctx.ME()):
                    value = var - value
                elif (ctx.MUE()):
                    value = var * value
                elif (ctx.DE()):
                    value = var / value

        if (ctx.SOPEN()):
            var = self.symbol_table.getSymbol(name=label)
            if (not isinstance(var, list)):
                self.error("Appending to a list requires the variable being a list")
                return
            var.append(value)
            tval = value
            value = var
            # TODO: Double check that this still works
            self.symbol_table.putSymbol(symbol=Symbol(name=label, symbolType=SYMBOL_VARIABLE, value=value))
            # self.data.storeVar(label, value)
            if (isinstance(tval, threading.Thread)):
                tval.label = label + "." + str(len(value) - 1)
                tval.start()
        else:
            self.symbol_table.putSymbol(symbol=Symbol(name=label, symbolType=SYMBOL_VARIABLE, value=value))
            if (isinstance(value, threading.Thread)):
                value.label = label
                value.start()

        if (self.appOptions.debug):
            self.log.log('> Assigning Variable: ' + label + ' = ' + str(
                self.symbol_table.getSymbol(name=label, symbolType=SYMBOL_VARIABLE)))
            self.log.log('')

    # Visit a parse tree produced by AhParser#flow.
    def visitFlow(self, ctx: AhParser.FlowContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by Ah3Parser#create_instance.
    def visitCreate_instance(self, ctx: AhParser.Create_instanceContext):
        label = self.visit(ctx.label())
        symbol: ScriptSymbol = self.symbol_table.getSymbol(name=label, symbolType=SYMBOL_SCRIPT)
        scriptax = symbol.driver.getDriverScript(symbol.path)
        parser = self.parseScript(scriptax)
        instanceTable: SymbolTable = parser.symbol_table
        instanceTable.resetTable()
        instanceTable.enterScope() #SymbolTable()
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
    def visitMethod_call(self, ctx: AhParser.Method_callContext):
        self.symbol_table.enterScope()
        self.symbol_table.current.setMeta(scopeType=SCOPE_METHOD)
        # TODO: Check to ensure that the passed parameters mesh with symbol_table.method_statement.value.optional_block
        # TODO: In the current scope we need to insert the parameters to the method
        # TODO: Check to see whether ASYNC should be used here
        label = self.visit(ctx.labels())
        labels = label.split('.')
        result = None

        if len(labels) < 2:
            # Executing a method on the current scope
            table: SymbolTable = createTableFromScope(self.symbol_table.root)
            table.deleteOnExit = True # Prevents hanging method & block scopes when debugging
            result = self.parseScriptCustom(self.symbol_table.getSymbol(name=labels[0]).value.block(), table)
        else:
            # Executing a method on an instance variable or imported script
            scope: SymbolScope = self.symbol_table.getSymbol(name=labels[0]).value
            table: SymbolTable = createTableFromScope(scope)
            table.deleteOnExit = True # Prevents hanging method & block scopes when debugging
            result = self.parseScriptCustom(scope.getSymbol(name=labels[1]).value.block(), table)
        self.symbol_table.exitScopeAndDelete() # This way we dont get a bunch of hanging method scopes when we debug
        return result

    # Visit a parse tree produced by AhParser#if_statement.
    def visitIf_statement(self, ctx: AhParser.If_statementContext):

        i = 0

        while (True):
            if (ctx.condition(i) is None):
                if (ctx.ELSE()):
                    return self.visit(ctx.block(i))
                else:
                    return None
            condition = self.visit(ctx.condition(i))
            if (condition):
                return self.visit(ctx.block(i))
            else:
                i += 1

    # Visit a parse tree produced by AhParser#while_statement.
    def visitWhile_statement(self, ctx: AhParser.While_statementContext):
        while (self.visit(ctx.condition())):
            self.visit(ctx.block())

    # Visit a parse tree produced by AhParser#for_statement.
    def visitFor_statement(self, ctx: AhParser.For_statementContext):
        clause = self.visit(ctx.expr())
        label = self.visit(ctx.labels())

        if (isinstance(clause, str) and isJson(clause)):
            clause = json.loads(clause)

        if (isinstance(clause, list)):
            if (self.appOptions.debug):
                self.log.log('> Looping through list with var ' + label)
                self.log.log('')
            for item in clause:
                if (self.appOptions.debug):
                    self.log.log('>> Assigning ' + label + ' = ' + str(item))
                    self.log.log('')
                    self.log.log('')
                self.data.storeVar(label, item)
                self.visit(ctx.block())
            self.data.deleteVar(label)

        elif (isinstance(clause, float) or isinstance(clause, int)):
            if (self.appOptions.debug):
                self.log.log('> Looping through range with var ' + label)
                self.log.log('')
            for i in range(0, int(clause)):
                if (self.appOptions.debug):
                    self.log.log('>> Assigning ' + label + ' = ' + str(i))
                    self.log.log('')
                    self.log.log('')
                self.data.storeVar(label, i)
                self.visit(ctx.block())
            self.data.deleteVar(label)

        else:
            if (self.appOptions.debug):
                self.error('Invalid Loop Type: ' + str(type(clause)))
                self.log.log('')

    # Visit a parse tree produced by AhParser#each_statement.
    def visitEach_statement(self, ctx: AhParser.Each_statementContext):
        clause = self.visit(ctx.expr())

        if (isinstance(clause, str) and isJson(clause)):
            clause = json.loads(clause)

        if (isinstance(clause, list)):
            if (self.appOptions.debug):
                self.log.log('> Looping through result')
                self.log.log('')
            callback = self.visit(ctx.callback())
            for item in clause:
                if (self.appOptions.debug):
                    self.log.log('>> Assigning result = ' + str(item))
                    self.log.log('')
                    self.log.log('')
                self.executeIsolatedCallback(callback, item)
        else:
            self.error("An each loop must be passed a list")

    # Visit a parse tree produced by AhParser#condition.
    def visitCondition(self, ctx: AhParser.ConditionContext):
        condition = self.visit(ctx.expr())

        if (self.appOptions.debug):
            self.log.log('>> Evaluated Flow Condition as: ' + str(condition))
            self.log.log('')

        return condition

    # Visit a parse tree produced by AhParser#block.
    def visitBlock(self, ctx: AhParser.BlockContext):
        self.symbol_table.enterScope()
        self.symbol_table.current.setMeta(scopeType=SCOPE_BLOCK)
        temp = self.visitChildren(ctx)
        self.symbol_table.exitScope()
        return temp

    # Visit a parse tree produced by AhParser#callback.
    def visitCallback(self, ctx: AhParser.CallbackContext):
        parameters = {}
        if (ctx.optional_parameters_block()):
            parameters = self.visit(ctx.optional_parameters_block())
        return {"params": parameters, "block": ctx.callback_block()}

    # Visit a parse tree produced by AhParser#callback_block.
    def visitCallback_block(self, ctx: AhParser.Callback_blockContext):
        temp = self.visitChildren(ctx)
        return temp

    # Visit a parse tree produced by AhParser#optional_parameters_block.
    def visitOptional_parameters_block(self, ctx: AhParser.Optional_parameters_blockContext):
        i = 0
        parameters = {}
        while (ctx.optional_parameter(i)):
            opParam = self.visit(ctx.optional_parameter(i))
            parameters[opParam['label']] = opParam['value']
            i += 1
        return parameters

    # Visit a parse tree produced by Ah3Parser#sig_parameter_block.
    def visitSig_parameter_block(self, ctx: AhParser.Sig_parameter_blockContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by AhParser#sig_parameter.
    def visitSig_parameter(self, ctx: AhParser.Sig_parameterContext):
        if (ctx.labels()):
            return {"label": self.visit(ctx.labels())}
        else:
            return self.visit(ctx.optional_parameter())

    # Visit a parse tree produced by AhParser#call_parameter.
    def visitCall_parameter(self, ctx: AhParser.Call_parameterContext):
        if (ctx.expr()):
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
        driver = None

        if (not ctx.SCRIPT() and not ctx.COMMANDTAX()):
            command += "api"
            if (ctx.GET()):
                command += " --get"
            if (ctx.POST()):
                command += " --post"
            if (ctx.PUT()):
                command += " --put"
            if (ctx.PATCH()):
                command += " --patch"
            if (ctx.DELETE()):
                command += " --delete"
            command += " --url " + self.data.getUrl("current") + firstArg

        elif (ctx.SCRIPT()):
            command += "scriptax " + firstArg + " --apitax-script"

        elif (ctx.COMMANDTAX()):
            command = firstArg

        if (ctx.obj_dict()):
            dataArg = self.visit(ctx.obj_dict())
            if ('post' in dataArg):
                command += " --data-post '" + json.dumps(dataArg['post']) + "'"
            if ('query' in dataArg):
                command += " --data-query '" + json.dumps(dataArg['query']) + "'"
            if ('path' in dataArg):
                command += " --data-path '" + json.dumps(dataArg['path']) + "'"
            if ('header' in dataArg):
                command += " --data-header '" + json.dumps(dataArg['header']) + "'"
            if ('driver' in dataArg):
                command += " --apitax-driver " + dataArg['driver']
                driver = dataArg['driver']
            if ('strict' in dataArg):
                strict = bool(dataArg['strict'])
            if ('auth' in dataArg):
                credentials = dataArg['auth']

        i = 0
        parameters = {}
        while (ctx.optional_parameter(i)):
            opParam = self.visit(ctx.optional_parameter(i))
            parameters[opParam['label']] = opParam['value']
            i += 1

        return {'command': command, 'parameters': parameters, 'strict': strict, 'credentials': credentials,
                'driver': driver}

    # Visit a parse tree produced by AhParser#execute.
    def visitExecute(self, ctx):
        resolvedCommand = self.visit(ctx.commandtax())
        if (ctx.callback()):
            resolvedCommand['callback'] = self.visit(ctx.callback())
        return self.executeCommand(resolvedCommand)

    # Visit a parse tree produced by AhParser#async_execute.
    def visitAsync_execute(self, ctx: AhParser.Async_executeContext):
        resolvedCommand = self.visit(ctx.commandtax())
        if (ctx.callback()):
            resolvedCommand['callback'] = self.visit(ctx.callback())
        thread = GenericExecution(self, "Async execution and callback", resolvedCommand, log=self.log,
                                  debug=self.appOptions.debug, sensitive=self.appOptions.sensitive)
        self.threads.append(thread)
        return thread

    # Visit a parse tree produced by AhParser#await.
    def await_statement(self):
        if (not ctx.labels()):
            for thread in self.threads:
                thread.join()
            return
        threads = self.getVariable(ctx.labels())
        if (isinstance(threads, list)):
            for thread in threads:
                if (isinstance(thread, threading.Thread)):
                    thread.join()
        elif (isinstance(threads, threading.Thread)):
            threads.join()

    # Visit a parse tree produced by AhParser#labels.
    def visitLabels(self, ctx: AhParser.LabelsContext):

        label = [self.visit(ctx.label_comp(0))]
        i = 0
        while (ctx.DOT(i)):
            label.append(str(self.visit(ctx.label_comp(i + 1))))
            i += 1

        label = '.'.join(label)

        return label.replace('$', '')

    # Visit a parse tree produced by AhParser#label_comp.
    def visitLabel_comp(self, ctx: AhParser.Label_compContext):
        if (ctx.label()):
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
        return self.visitChildren(ctx)

    # Visit a parse tree produced by AhParser#params_statement.
    def visitSig_statement(self, ctx: AhParser.Sig_statementContext):
        i = 0
        while (ctx.sig_parameter(i)):
            sigItem = self.visit(ctx.sig_parameter(i))

            if (self.data.isVarExist('params.passed.' + sigItem['label'])):
                self.data.storeVar('params.' + sigItem['label'], self.data.getVar('params.passed.' + sigItem['label']))
            elif ('value' in sigItem):
                self.data.storeVar('params.' + sigItem['label'], sigItem['value'])
            else:
                self.error(
                    'Insufficient parameters. Expected Parameter: \'' + str(sigItem['label']) + '\'')

            i += 1

    # Visit a parse tree produced by AhParser#options_statement.
    def visitOptions_statement(self, ctx: AhParser.Options_statementContext):
        self.options = self.visit(ctx.expr())
        self.useOptions()

    # Visit a parse tree produced by AhParser#delete_statement.
    def visitDelete_statement(self, ctx: AhParser.Delete_statementContext):
        label = self.visit(ctx.labels())
        self.data.deleteVar(label)
        if (self.appOptions.debug):
            self.log.log('> Deleteing variable: ' + label)
            self.log.log('')

    # Visit a parse tree produced by AhParser#error_statement.
    def visitError_statement(self, ctx: AhParser.Error_statementContext):
        message = "No error message was specified"
        if (ctx.expr()):
            message = self.visit(ctx.expr())
        self.error(message)

    # Visit a parse tree produced by AhParser#return_statement.
    def visitReturn_statement(self, ctx: AhParser.Return_statementContext):
        exportation = ""
        if (ctx.expr()):
            exportation = self.visit(ctx.expr())
            self.data.setReturn(exportation)
        else:
            self.data.setReturn({})
        self.data.setFlow('return', True)
        if (self.appOptions.debug):
            if (exportation != ""):
                self.log.log('> Returning with value: ' + str(exportation))
            else:
                self.log.log('> Returning ')
            self.log.log('')

    # Visit a parse tree produced by AhParser#login_statement.
    def visitLogin_statement(self, ctx: AhParser.Login_statementContext):
        from apitaxcore.flow.Connector import Connector

        parameters = self.visit(ctx.optional_parameters_block())

        driver = self.appOptions.driver
        extra = {}

        if ('driver' in parameters):
            driver = parameters['driver']

        if ('extra' in parameters):
            extra = parameters['extra']

        if ('username' in parameters and 'password' in parameters):
            if (self.appOptions.debug):
                self.log.log("> Logging into API with username and password.")
                self.log.log("")
            connector = Connector(options=Options(debug=self.appOptions.debug, sensitive=True, driver=driver),
                                  credentials=Credentials(username=parameters['username'],
                                                          password=parameters['password'], extra=extra))
            return connector.credentials
        elif ('token' in parameters):
            return Credentials(token=parameters['token'])
        else:
            self.error('Must pass a `username` and `password` or a `token` for authentication')
            return None

    # Visit a parse tree produced by AhParser#endpoint_statement.
    def visitEndpoint_statement(self, ctx: AhParser.Endpoint_statementContext):
        name = self.visit(ctx.expr())
        try:
            name.find('@')
            name = name.split('@')
            driver = LoadedDrivers.getDriver(name[1])
            name = name[0]
        except:
            if (self.appOptions.driver):
                driver = LoadedDrivers.getDriver(self.appOptions.driver)
            else:
                driver = LoadedDrivers.getDefaultDriver()
        endpoints = driver.getEndpointCatalog()['endpoints']
        if (name in endpoints):
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
        parser = self.parseScript(scriptax)
        importTable: SymbolTable = parser.symbol_table
        importTable.resetTable()
        importTable.enterScope() #SymbolTable()
        importScope = importTable.current
        importScope.setMeta(name=name, scopeType=SCOPE_SCRIPT)

        # Insert the script scope into our scope and add a symbol to reference it
        reference = self.symbol_table.current.parent.insertScope(importScope)
        #self.symbol_table.exitScope()
        self.symbol_table.current.addSymbol(symbol=ScriptSymbol(name=name, symbolType=SYMBOL_SCRIPT, dataType=DATA_SCRIPT, value=reference, path=path, driver=driver))
        #return self.visitChildren(ctx)

    # Visit a parse tree produced by AhParser#casting.
    def visitCasting(self, ctx: AhParser.CastingContext):
        value = self.visit(ctx.expr())
        returner = None
        if (ctx.TYPE_INT()):
            returner = int(value)
            if (self.appOptions.debug):
                self.log.log('> Explicitly Casting \'' + str(value) + '\' to int: ' + json.dumps(returner))
                self.log.log('')
            return returner

        if (ctx.TYPE_DEC()):
            returner = float(value)
            if (self.appOptions.debug):
                self.log.log('> Explicitly Casting \'' + str(value) + '\' to number: ' + json.dumps(returner))
                self.log.log('')
            return returner

        if (ctx.TYPE_BOOL()):
            returner = bool(value)
            if (self.appOptions.debug):
                self.log.log('> Explicitly Casting \'' + str(value) + '\' to boolean: ' + json.dumps(returner))
                self.log.log('')
            return returner

        if (ctx.TYPE_STR()):
            returner = str(value)
            if (self.appOptions.debug):
                self.log.log('> Explicitly Casting \'' + str(value) + '\' to string: ' + json.dumps(returner))
                self.log.log('')
            return returner

        if (ctx.TYPE_LIST()):
            returner = list(str(value).split(","))
            if (self.appOptions.debug):
                self.log.log('> Explicitly Casting \'' + str(value) + '\' to list: ' + json.dumps(returner))
                self.log.log('')
            return returner

        if (ctx.TYPE_DICT()):
            if (isinstance(value, dict)):
                returner = value
            elif (isinstance(value, list)):
                count = 0
                newdict = {}
                for i in value:
                    newdict.update({str(count): i})
                    count += 1
                returner = dict(newdict)
            elif (isinstance(value, str) and isJson(value)):
                returner = dict(json.loads(str(value)))
            else:
                returner = dict({"default": value})

            if (self.appOptions.debug):
                self.log.log('> Explicitly Casting \'' + str(value) + '\' to dictionary: ' + json.dumps(returner))
                self.log.log('')

        return returner

    # Visit a parse tree produced by AhParser#auth.
    def visitAuth(self, ctx: AhParser.AuthContext):
        credentials = self.visit(ctx.expr())
        self.credentials = credentials
        if (self.appOptions.debug):
            self.log.log("> Setting active auth credentials to user: " + credentials.username)
            self.log.log("")

    # Visit a parse tree produced by AhParser#url.
    def visitUrl(self, ctx: AhParser.UrlContext):
        url = self.visit(ctx.expr())
        self.data.storeUrl("current", url)

        if (self.appOptions.debug):
            self.log.log('> Setting URL: ' + url)
            self.log.log('')

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
        return self.visitChildren(ctx)

    # Visit a parse tree produced by AhParser#inject.
    def visitInject(self, ctx: AhParser.InjectContext):
        returner = self.visit(ctx.expr())
        if (self.appOptions.debug):
            self.log.log('> Injecting into: ' + ctx.getText() + ' with the value ' + str(returner))
            self.log.log('')
        return returner

    # Visit a parse tree produced by AhParser#atom.
    def visitAtom(self, ctx: AhParser.AtomContext):

        if (ctx.atom_obj_dict()):
            return self.visit(ctx.atom_obj_dict())

        if (ctx.atom_obj_list()):
            return self.visit(ctx.atom_obj_list())

        if (ctx.atom_string()):
            return self.visit(ctx.atom_string())

        if (ctx.atom_number()):
            return self.visit(ctx.atom_number())

        if (ctx.atom_boolean()):
            return self.visit(ctx.atom_boolean())

        if (ctx.atom_hex()):
            return self.visit(ctx.atom_hex())

        if (ctx.atom_none()):
            return self.visit(ctx.atom_none())

    # Visit a parse tree produced by AhParser#obj_dict.
    def visitAtom_obj_dict(self, ctx: AhParser.Atom_obj_dictContext):
        dictionary = {}
        i = 0
        if (ctx.COLON(0)):
            dictionary[self.visit(ctx.expr(0))] = self.visit(ctx.expr(1))
        while (ctx.COMMA(i) and ctx.expr((i + 1) * 2)):
            base = (i + 1) * 2
            dictionary[self.visit(ctx.expr(base))] = self.visit(ctx.expr(base + 1))
            i += 1
        return dictionary

    # Visit a parse tree produced by AhParser#obj_list.
    def visitAtom_obj_list(self, ctx: AhParser.Atom_obj_listContext):
        parameters = []
        i = 0
        if (ctx.expr(0)):
            parameters.append(self.visit(ctx.expr(0)))
        while (ctx.COMMA(i) and ctx.expr(i + 1)):
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
            if (self.appOptions.debug):
                self.log.log('> Injecting Variable into String \'' + label + '\': ' + line)
                self.log.log('')
        return line

    # Visit a parse tree produced by AhParser#number.
    def visitAtom_number(self, ctx: AhParser.Atom_numberContext):
        if (ctx.INT()):
            return int(ctx.INT().getText())
        else:
            return float(ctx.FLOAT().getText())

    # Visit a parse tree produced by AhParser#boolean.
    def visitAtom_boolean(self, ctx: AhParser.Atom_booleanContext):
        if (ctx.TRUE()):
            return True
        if (ctx.FALSE()):
            return False

    # Visit a parse tree produced by Ah3Parser#atom_hex.
    def visitAtom_hex(self, ctx: AhParser.Atom_hexContext):
        return '0x' + str(ctx.HEX().getText())[2:].upper()

    # Visit a parse tree produced by Ah3Parser#atom_none.
    def visitAtom_none(self, ctx: AhParser.Atom_noneContext):
        return None
