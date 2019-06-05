from scriptax.tests.pre_test import execute


def test_none():
    scriptax = '''
    test = null;
    return test;
    '''
    block_status, visitor = execute(scriptax)
    assert block_status.result == None