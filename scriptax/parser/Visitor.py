from apitax.grammar.build.Ah210Parser import Ah210Parser
from apitax.grammar.build.Ah210Visitor import Ah210Visitor as Ah210VisitorOriginal
from apitax.ah.scriptax.ScriptData import ScriptData as DataStore
from apitax.ah.models.State import State
from apitax.utilities.Async import GenericExecution
from apitax.utilities.Json import isJson
from apitax.ah.flow.LoadedDrivers import LoadedDrivers
from apitax.ah.models.Credentials import Credentials
from apitax.ah.models.Options import Options

import json
import re
import threading


class AhVisitor(Ah210VisitorOriginal):

    def __init__(self, credentials: Credentials = Credentials(), parameters={}, options: Options = Options(), file=''):
        self.data = DataStore()
        self.log = State.log
        self.appOptions = options
        self.config = State.config
        self.parser = None
        self.options = {}
        self.credentials = credentials
        self.data.storeVar("params.passed", parameters)
        self.state = {'file': file, 'line': 0, 'char': 0}
        self.threads = []

        # Replace the below functionality if possible
        self.regexVar = '{{[ ]{0,}[A-z0-9_$.\-]{1,}[ ]{0,}}}'

    def setState(self, file='', line=-1, char=-1):
        if (file != ''):
            self.state['file'] = file
        if (line != -1):
            self.state['line'] = line
        if (char != -1):
            self.state['char'] = char

    def importCommandRequest(self, commandHandler, export=False):
        from apitax.ah.commandtax.commands.Custom import Custom as CustomCommand

        if (commandHandler.getRequest().getResponseBody().strip() != ''):
            if (not isinstance(commandHandler.getRequest(), CustomCommand)):
                self.data.importScriptsExports(commandHandler.getRequest().parser.data, export=export)
            else:
                self.data.storeRequest(commandHandler.getRequest().getResponseBody(), export=export)

    def executeCommand(self, resolvedCommand, logPrefix=''):
        from apitax.ah.flow.Connector import Connector
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

    def getVariable(self, label, isRequest=False, convert=True):
        if (convert):
            label = self.visit(label)
        try:
            if (isRequest):
                return self.data.getRequest(label)
            else:
                return self.data.getVar(label)
        except:

            return None

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

    def inject(self, line):
        matches = re.findall(self.regexVar, line)
        for match in matches:
            label = match[2:-2].strip()
            replacer = self.getVariable(label, convert=False)
            line = line.replace(match, replacer)
        return line

    def executeIsolatedCallback(self, callback, resultScope, logPrefix=''):
        visitor = AhVisitor(options=Options(debug=self.appOptions.debug, sensitive=self.appOptions.sensitive))
        visitor.setState(file=self.state['file'])
        visitor.log.prefix = logPrefix
        visitor.data.storeVar('result', resultScope)
        for key, value in callback['params'].items():
            visitor.data.storeVar(key, value)
        block = callback['block']
        callbackResult = visitor.visit(block)
        return visitor.data.getVar('result')

    def error(self, message, logprefix=''):
        self.data.error(message, logprefix=logprefix)

    def isError(self):
        return self.data.getFlow('error')

    def isExit(self):
        return self.data.getFlow('exit')

    def isReturn(self):
        return self.data.getFlow('return')

    # Visit a parse tree produced by Ah210Parser#prog.
    def visitProg(self, ctx):
        self.parser = ctx.parser
        temp = self.visitChildren(ctx)

        if (self.isError()):
            error = self.isError()
            self.log.error(
                error['message'] + ' in ' + str(self.state['file']) + ' @' + str(self.state['line']) + ':' + str(
                    self.state['char']), prefix=error['logprefix'])
            if (self.appOptions.debug):
                self.log.log('')
                self.log.log('')

        return self

    # Visit a parse tree produced by Ah210Parser#statements.
    def visitStatements(self, ctx):
        if (self.isReturn() or self.isError()):
            return
        temp = self.visitChildren(ctx)
        return temp

    # Visit a parse tree produced by Ah210Parser#statement.
    def visitStatement(self, ctx):
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

    # Visit a parse tree produced by Ah210Parser#terminated.
    def visitTerminated(self, ctx: Ah210Parser.TerminatedContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by Ah210Parser#non_terminated.
    def visitNon_terminated(self, ctx: Ah210Parser.Non_terminatedContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by Ah210Parser#executers.
    def visitExecuters(self, ctx: Ah210Parser.ExecutersContext):
        if (ctx.execute()):
            return self.visit(ctx.execute())
        if (ctx.async_execute()):
            thread = self.visit(ctx.async_execute())
            thread.start()
            return thread

    # Visit a parse tree produced by Ah210Parser#expr.
    def visitExpr(self, ctx):  # Get number of terms and loop this code for #terms - 1
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
            return self.getVariable(ctx.labels(), isRequest=ctx.REQUEST())

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

    # Visit a parse tree produced by Ah210Parser#set_var.
    def visitAssignment(self, ctx: Ah210Parser.AssignmentContext):
        label = self.visit(ctx.labels())
        value = None

        if (ctx.expr()):
            value = self.visit(ctx.expr())

        if (not ctx.EQUAL()):
            var = self.data.getVar(label)
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
            var = self.data.getVar(label)
            if (not isinstance(var, list)):
                self.error("Appending to a list requires the variable being a list")
                return
            var.append(value)
            tval = value
            value = var
            self.data.storeVar(label, value)
            if (isinstance(tval, threading.Thread)):
                tval.label = label + "." + str(len(value) - 1)
                tval.start()
        else:
            self.data.storeVar(label, value)
            if (isinstance(value, threading.Thread)):
                value.label = label
                value.start()

        if (self.appOptions.debug):
            self.log.log('> Assigning Variable: ' + label + ' = ' + str(self.data.getVar(label)))
            self.log.log('')

    # Visit a parse tree produced by Ah210Parser#flow.
    def visitFlow(self, ctx: Ah210Parser.FlowContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by Ah210Parser#if_statement.
    def visitIf_statement(self, ctx: Ah210Parser.If_statementContext):

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

    # Visit a parse tree produced by Ah210Parser#while_statement.
    def visitWhile_statement(self, ctx: Ah210Parser.While_statementContext):
        while (self.visit(ctx.condition())):
            self.visit(ctx.block())

    # Visit a parse tree produced by Ah210Parser#for_statement.
    def visitFor_statement(self, ctx: Ah210Parser.For_statementContext):
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

    # Visit a parse tree produced by Ah210Parser#each_statement.
    def visitEach_statement(self, ctx: Ah210Parser.Each_statementContext):
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

    # Visit a parse tree produced by Ah210Parser#condition.
    def visitCondition(self, ctx: Ah210Parser.ConditionContext):
        condition = self.visit(ctx.expr())

        if (self.appOptions.debug):
            self.log.log('>> Evaluated Flow Condition as: ' + str(condition))
            self.log.log('')

        return condition

    # Visit a parse tree produced by Ah210Parser#block.
    def visitBlock(self, ctx: Ah210Parser.BlockContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by Ah210Parser#callback.
    def visitCallback(self, ctx: Ah210Parser.CallbackContext):
        parameters = {}
        if (ctx.optional_parameters_block()):
            parameters = self.visit(ctx.optional_parameters_block())
        return {"params": parameters, "block": ctx.callback_block()}

    # Visit a parse tree produced by Ah210Parser#callback_block.
    def visitCallback_block(self, ctx: Ah210Parser.Callback_blockContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by Ah210Parser#optional_parameters_block.
    def visitOptional_parameters_block(self, ctx: Ah210Parser.Optional_parameters_blockContext):
        i = 0
        parameters = {}
        while (ctx.optional_parameter(i)):
            opParam = self.visit(ctx.optional_parameter(i))
            parameters[opParam['label']] = opParam['value']
            i += 1
        return parameters

    # Visit a parse tree produced by Ah210Parser#sig_parameter.
    def visitSig_parameter(self, ctx: Ah210Parser.Sig_parameterContext):
        if (ctx.labels()):
            return {"label": self.visit(ctx.labels())}
        else:
            return self.visit(ctx.optional_parameter())

    # Visit a parse tree produced by Ah210Parser#call_parameter.
    def visitCall_parameter(self, ctx: Ah210Parser.Call_parameterContext):
        if (ctx.expr()):
            return {"value": self.visit(ctx.expr())}
        else:
            return self.visit(ctx.optional_parameter())

    # Visit a parse tree produced by Ah210Parser#optional_parameter.
    def visitOptional_parameter(self, ctx: Ah210Parser.Optional_parameterContext):
        return {"label": self.visit(ctx.labels()), "value": self.visit(ctx.expr())}

    # Visit a parse tree produced by Ah210Parser#commandtax.
    def visitCommandtax(self, ctx: Ah210Parser.CommandtaxContext):
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

    # Visit a parse tree produced by Ah210Parser#execute.
    def visitExecute(self, ctx):
        resolvedCommand = self.visit(ctx.commandtax())
        if (ctx.callback()):
            resolvedCommand['callback'] = self.visit(ctx.callback())
        return self.executeCommand(resolvedCommand)

    # Visit a parse tree produced by Ah210Parser#async_execute.
    def visitAsync_execute(self, ctx: Ah210Parser.Async_executeContext):
        resolvedCommand = self.visit(ctx.commandtax())
        if (ctx.callback()):
            resolvedCommand['callback'] = self.visit(ctx.callback())
        thread = GenericExecution(self, "Async execution and callback", resolvedCommand, log=self.log,
                                  debug=self.appOptions.debug, sensitive=self.appOptions.sensitive)
        self.threads.append(thread)
        return thread

    # Visit a parse tree produced by Ah210Parser#await.
    def visitAwait(self, ctx: Ah210Parser.AwaitContext):
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

    # Visit a parse tree produced by Ah210Parser#labels.
    def visitLabels(self, ctx: Ah210Parser.LabelsContext):

        label = [self.visit(ctx.label_comp(0))]
        i = 0
        while (ctx.DOT(i)):
            label.append(str(self.visit(ctx.label_comp(i + 1))))
            i += 1

        label = '.'.join(label)

        return label.replace('$', '')

    # Visit a parse tree produced by Ah210Parser#label_comp.
    def visitLabel_comp(self, ctx: Ah210Parser.Label_compContext):
        if (ctx.LABEL()):
            return ctx.LABEL().getText()
        else:
            return self.visit(ctx.inject())

    # Visit a parse tree produced by Ah210Parser#params_statement.
    def visitParams_statement(self, ctx: Ah210Parser.Params_statementContext):
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

    # Visit a parse tree produced by Ah210Parser#options_statement.
    def visitOptions_statement(self, ctx: Ah210Parser.Options_statementContext):
        self.options = self.visit(ctx.expr())
        self.useOptions()

    # Visit a parse tree produced by Ah210Parser#delete_statement.
    def visitDelete_statement(self, ctx: Ah210Parser.Delete_statementContext):
        label = self.visit(ctx.labels())
        self.data.deleteVar(label)
        if (self.appOptions.debug):
            self.log.log('> Deleteing variable: ' + label)
            self.log.log('')

    # Visit a parse tree produced by Ah210Parser#error_statement.
    def visitError_statement(self, ctx: Ah210Parser.Error_statementContext):
        message = "No error message was specified"
        if (ctx.expr()):
            message = self.visit(ctx.expr())
        self.error(message)

    # Visit a parse tree produced by Ah210Parser#return_statement.
    def visitReturn_statement(self, ctx: Ah210Parser.Return_statementContext):
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

    # Visit a parse tree produced by Ah210Parser#login_statement.
    def visitLogin_statement(self, ctx: Ah210Parser.Login_statementContext):
        from apitax.ah.flow.Connector import Connector

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

    # Visit a parse tree produced by Ah210Parser#endpoint_statement.
    def visitEndpoint_statement(self, ctx: Ah210Parser.Endpoint_statementContext):
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

    # Visit a parse tree produced by Ah210Parser#scoping.
    def visitScoping(self, ctx):
        # print('scoping')
        return self.visitChildren(ctx)

    # Visit a parse tree produced by Ah210Parser#name.
    def visitName(self, ctx):
        if ctx.expr():
            self.data.name = self.visit(ctx.expr())

        if (self.appOptions.debug):
            self.log.log('> Setting Script Name: ' + self.data.name)
            self.log.log('')

    # Visit a parse tree produced by Ah210Parser#exports.
    def visitExports(self, ctx):

        exportation = ""

        if (ctx.labels()):
            exportation = self.visit(ctx.labels())
            self.data.exportVar(exportation)

        if (ctx.execute()):
            commandHandler = self.visit(ctx.execute())
            self.importCommandRequest(commandHandler['commandHandler'], export=True)
            exportation = commandHandler['command']

        if (self.appOptions.debug):
            self.log.log('> Exporting: ' + exportation)
            self.log.log('')

    # Visit a parse tree produced by Ah210Parser#imports.
    def visitImports(self, ctx):

        commandHandler = self.visit(ctx.execute())['commandHandler']
        self.importCommandRequest(commandHandler)

        if (self.appOptions.debug):
            self.log.log('> Importing: ' + commandHandler)
            self.log.log('')

    # Visit a parse tree produced by Ah210Parser#casting.
    def visitCasting(self, ctx: Ah210Parser.CastingContext):
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

    # Visit a parse tree produced by Ah210Parser#auth.
    def visitAuth(self, ctx: Ah210Parser.AuthContext):
        credentials = self.visit(ctx.expr())
        self.credentials = credentials
        if (self.appOptions.debug):
            self.log.log("> Setting active auth credentials to user: " + credentials.username)
            self.log.log("")

    # Visit a parse tree produced by Ah210Parser#url.
    def visitUrl(self, ctx: Ah210Parser.UrlContext):
        url = self.visit(ctx.expr())
        self.data.storeUrl("current", url)

        if (self.appOptions.debug):
            self.log.log('> Setting URL: ' + url)
            self.log.log('')

    # Visit a parse tree produced by Ah210Parser#log.
    def visitLog(self, ctx: Ah210Parser.LogContext):
        if (ctx.expr()):
            self.log.log('> Logging: ' + json.dumps(self.visit(ctx.expr())))
            self.log.log('')

    # Visit a parse tree produced by Ah210Parser#count.
    def visitCount(self, ctx: Ah210Parser.CountContext):
        return len(self.visit(ctx.expr()))

    # Visit a parse tree produced by Ah210Parser#inject.
    def visitInject(self, ctx: Ah210Parser.InjectContext):
        returner = self.visit(ctx.expr())
        if (self.appOptions.debug):
            self.log.log('> Injecting into: ' + ctx.getText() + ' with the value ' + str(returner))
            self.log.log('')
        return returner

    # Visit a parse tree produced by Ah210Parser#atom.
    def visitAtom(self, ctx: Ah210Parser.AtomContext):
        if (ctx.obj_dict()):
            return self.visit(ctx.obj_dict())

        if (ctx.obj_list()):
            return self.visit(ctx.obj_list())

        if (ctx.string()):
            return self.visit(ctx.string())

        if (ctx.number()):
            return self.visit(ctx.number())

        if (ctx.boolean()):
            return self.visit(ctx.boolean())

    # Visit a parse tree produced by Ah210Parser#obj_dict.
    def visitObj_dict(self, ctx: Ah210Parser.Obj_dictContext):
        dictionary = {}
        i = 0
        if (ctx.COLON(0)):
            dictionary[self.visit(ctx.expr(0))] = self.visit(ctx.expr(1))
        while (ctx.COMMA(i) and ctx.expr((i + 1) * 2)):
            base = (i + 1) * 2
            dictionary[self.visit(ctx.expr(base))] = self.visit(ctx.expr(base + 1))
            i += 1
        return dictionary

    # Visit a parse tree produced by Ah210Parser#obj_list.
    def visitObj_list(self, ctx: Ah210Parser.Obj_listContext):
        parameters = []
        i = 0
        if (ctx.expr(0)):
            parameters.append(self.visit(ctx.expr(0)))
        while (ctx.COMMA(i) and ctx.expr(i + 1)):
            parameters.append(self.visit(ctx.expr(i + 1)))
            i += 1
        return parameters

    # Visit a parse tree produced by Ah210Parser#string.
    def visitString(self, ctx: Ah210Parser.StringContext):
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

    # Visit a parse tree produced by Ah210Parser#number.
    def visitNumber(self, ctx: Ah210Parser.NumberContext):
        if (ctx.INT()):
            return int(ctx.INT().getText())
        else:
            return float(ctx.FLOAT().getText())

    # Visit a parse tree produced by Ah210Parser#boolean.
    def visitBoolean(self, ctx: Ah210Parser.BooleanContext):
        if (ctx.TRUE()):
            return True
        if (ctx.FALSE()):
            return False