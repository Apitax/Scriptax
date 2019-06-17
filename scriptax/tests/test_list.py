from scriptax.tests.pre_test import execute


def test_list():
    scriptax = '''
    test = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10];
    return test;
    '''
    block_status, visitor = execute(scriptax)
    assert block_status.result == [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]


def test_list_2():
    scriptax = '''
    test = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, "something", true, false, null];
    return test;
    '''
    block_status, visitor = execute(scriptax)
    assert block_status.result == [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, "something", True, False, None]


def test_list_3():
    scriptax = '''
    test = [];
    return test;
    '''
    block_status, visitor = execute(scriptax)
    assert block_status.result == []


def test_list_access():
    scriptax = '''
    test = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10];
    return test.0;
    '''
    block_status, visitor = execute(scriptax)
    assert block_status.result == 0


def test_list_access_2():
    scriptax = '''
    test = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10];
    return test.10;
    '''
    block_status, visitor = execute(scriptax)
    assert block_status.result == 10


def test_list_access_3():
    scriptax = '''
    test = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10];
    return test.5;
    '''
    block_status, visitor = execute(scriptax)
    assert block_status.result == 5
