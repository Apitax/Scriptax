from scriptax.tests.pre_test import execute


def test_int():
    scriptax = '''
    test = 5;
    return test;
    '''
    block_status, visitor = execute(scriptax)
    assert block_status.result == 5


def test_negative_int():
    scriptax = '''
    test = -509;
    return test;
    '''
    block_status, visitor = execute(scriptax)
    assert block_status.result == -509


def test_big_int():
    scriptax = '''
    test = 5099327593287521432626;
    return test;
    '''
    block_status, visitor = execute(scriptax)
    assert block_status.result == 5099327593287521432626