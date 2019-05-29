import threading
import uuid
from apitaxcore.models.Options import Options
from scriptax.parser.utils.BoilerPlate import customizable_context_parser
from scriptax.parser.Visitor import AhVisitor
from scriptax.models.Parameter import Parameter
from typing import List


class GenericExecution(threading.Thread):
    def __init__(self, name, parent_visitor: AhVisitor, body_context, options: Options,
                 body_parameters: List[Parameter] = None, callback_context=None,
                 callback_parameters: List[Parameter] = None,
                 log=None, result_label: str = None):
        super().__init__()
        self.threadId = uuid.uuid4()
        self.name = name
        self.log = log
        self.options: Options = options
        self.result_label: str = result_label
        self.body_context = body_context
        self.body_parameters: List[Parameter] = body_parameters
        self.callback_context = callback_context
        self.callback_parameters: List[Parameter] = callback_parameters
        self.parent_visitor: AhVisitor = parent_visitor

    def run(self):
        if self.log and self.options.debug:
            self.log.log(">> Executing Async")
            self.log.log('')

        # Execute command
        result = customizable_context_parser(context=self.body_context, parameters=self.body_parameters,
                                             options=self.options)

        if self.callback_context:
            result = customizable_context_parser(context=self.callback_context, parameters=self.callback_parameters + [
                Parameter(name="result", value=result[0], options=self.options)])

        if self.result_label:
            self.parent_visitor.set_variable(label=self.result_label, value=result[0])

    def serialize(self):
        return str(self.threadId)
