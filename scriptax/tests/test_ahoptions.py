from scriptax.tests.pre_test import execute


def test_ahoptions():
    scriptax = '''
    ahoptions({});
    return @self;
    '''
    block_status, visitor = execute(scriptax)
    addr_self = block_status.result['scope']['address']
    assert block_status.result == {'scope': {'name': 'main', 'scope-type': 'module', 'address': addr_self, 'attributes': {'name': '', 'help': '', 'summary': '', 'description': '', 'author': '', 'version': '', 'link': '', 'available': True, 'enabled': True, 'access': []}, 'symbols': [], 'dynamic_links': {'caller': {}, 'calling': {}}, 'static_links': {'parent': {}, 'children': []}}}


def test_ahoptions_2():
    scriptax = '''
    ahoptions({
        "name": "test",
        "help": "help",
        "summary": "summary",
        "description": "description",
        "author": "author",
        "version": "1.2.3",
        "link": "http://google.com?test=6&y=hello",
        "available": true,
        "enabled": false,
        "access": ["admin", "developer"],
    });
    return @self;
    '''
    block_status, visitor = execute(scriptax)
    addr_self = block_status.result['scope']['address']
    assert block_status.result == {'scope': {'name': 'main', 'scope-type': 'module', 'address': addr_self, 'attributes': {'name': 'test', 'help': 'help', 'summary': 'summary', 'description': 'description', 'author': 'author', 'version': '1.2.3', 'link': 'http://google.com?test=6&y=hello', 'available': True, 'enabled': False, 'access': ['admin', 'developer']}, 'symbols': [], 'dynamic_links': {'caller': {}, 'calling': {}}, 'static_links': {'parent': {}, 'children': []}}}


def test_ahoptions_3():
    scriptax = '''
    ahoptions({
        "unexpected": null,
    });
    return @self;
    '''
    block_status, visitor = execute(scriptax)
    addr_self = block_status.result['scope']['address']
    assert block_status.result == {'scope': {'name': 'main', 'scope-type': 'module', 'address': addr_self, 'attributes': {'name': '', 'help': '', 'summary': '', 'description': '', 'author': '', 'version': '', 'link': '', 'available': True, 'enabled': True, 'access': []}, 'symbols': [], 'dynamic_links': {'caller': {}, 'calling': {}}, 'static_links': {'parent': {}, 'children': []}}}
