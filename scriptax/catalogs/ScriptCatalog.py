from apitaxcore.catalog.Catalog import Catalog


class ScriptCatalog(Catalog):

    def __init__(self):
        super().__init__("scripts")

    def add(self, label, path, summary='', help='', driver='', examples=[]):
        item = {'label': label, 'path': path, 'summary': summary, 'help': help, 'driver': driver, 'examples': examples}
        super().add(item)
