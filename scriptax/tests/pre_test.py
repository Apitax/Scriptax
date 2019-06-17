from apitaxcore.logs.Log import Log
from apitaxcore.logs.StandardLog import StandardLog
from apitaxcore.models.State import State
from apitaxcore.models.Options import Options
from apitaxcore.flow.LoadedDrivers import LoadedDrivers
from apitaxcore.drivers.Drivers import Drivers
from scriptax.parser.utils.BoilerPlate import customizable_parser, read_string
from scriptax.drivers.builtin.Scriptax import Scriptax
from scriptax.models.BlockStatus import BlockStatus
from typing import Tuple
from scriptax.parser.Visitor import AhVisitor

State.log = Log(StandardLog(), logColorize=False)
State.log.log("")

Drivers.add("scriptax", Scriptax())
LoadedDrivers.load("scriptax")


def execute(scriptax: str) -> Tuple[BlockStatus, AhVisitor]:
    return customizable_parser(read_string(scriptax), file='inline_program', options=Options(debug=True))
