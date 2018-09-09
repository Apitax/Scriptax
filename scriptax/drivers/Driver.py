from apitaxcore.flow.responses.ApitaxResponse import ApitaxResponse
from commandtax.drivers.Driver import Driver as CommandtaxDriver
from commandtax.models.Command import Command
from scriptax.catalogs.ScriptCatalog import ScriptCatalog


# Base class for driver plugs
# Defines many customizable properties for interfacing to a new API type
class Driver(CommandtaxDriver):
    def isDriverScriptable(self) -> bool:
        return False

    # If driver is scriptable, returns the driver script catalog
    def getDriverScriptCatalog(self) -> ScriptCatalog:
        return ScriptCatalog()

    # Returns the contents of a script
    def getDriverScript(self, path) -> str:
        return ''

    # Renames a script
    def renameDriverScript(self, original, now) -> bool:
        return False

    # Creates/Updates a scripts content
    def saveDriverScript(self, path, content) -> bool:
        return False

    # Deletes a script
    def deleteDriverScript(self, path) -> bool:
        return False

    # Driver script handler
    def handleDriverScript(self, command: Command) -> ApitaxResponse:
        return ApitaxResponse()

    # Event handler fired before the driver script handler executes
    def onPreHandleDriverScript(self, command: Command) -> Command:
        return command