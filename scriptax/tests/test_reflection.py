from scriptax.tests.pre_test import execute


def test_reflection():
    scriptax = '''
    test = {"test": "worked", "test2": [{"yes": "no"}, {"day": "night"}, {"weekend": ["sunday", {"name": "saturday", "best_day": true}]}]};
    return @test;
    '''
    block_status, visitor = execute(scriptax)
    assert block_status.result == {'name': 'test', 'symbol-type': 'var', 'data-type': 'dict',
                                   'value': {'test': 'worked', 'test2': [{'yes': 'no'}, {'day': 'night'}, {'weekend': ['sunday', {'name': 'saturday', 'best_day': True}]}]},
                                   'attributes': {}}


def test_reflection_2():
    scriptax = '''
    return @self;
    '''
    block_status, visitor = execute(scriptax)
    print(block_status.result)
    addr_self = block_status.result['scope']['address']
    assert block_status.result == {'scope': {'name': 'main', 'scope-type': 'module', 'address': addr_self, 'attributes': {}, 'symbols': [], 'dynamic_links': {'caller': {}, 'calling': {}}, 'static_links': {'parent': {}, 'children': []}}}
