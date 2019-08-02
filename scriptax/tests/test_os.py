from scriptax.tests.pre_test import execute


def test_os():
    scriptax = '''
    test = os('scriptax', 'test_scriptax_access', param='test');
    return test;
    '''
    block_status, visitor = execute(scriptax)
    assert block_status.result == 'test worked'


def test_os_2():
    scriptax = '''
    test = os('scriptax', 'test_scriptax_access_2');
    return test;
    '''
    block_status, visitor = execute(scriptax)
    assert block_status.result == 'worked'
