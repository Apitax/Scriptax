from scriptax.tests.pre_test import execute


def test_boolean():
    scriptax = '''
    test = true;
    return test;
    '''
    block_status, visitor = execute(scriptax)
    assert block_status.result == True


def test_boolean2():
    scriptax = '''
    test = false;
    return test;
    '''
    block_status, visitor = execute(scriptax)
    assert block_status.result == False
