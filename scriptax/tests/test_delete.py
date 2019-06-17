from scriptax.tests.pre_test import execute


def test_delete():
    scriptax = '''
    test = "test";
    del(test);
    return test;
    '''
    try:
        block_status, visitor = execute(scriptax)
        assert False
    except:
        assert True


def test_delete_2():
    scriptax = '''
    test = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10];
    del(test);
    '''
    try:
        block_status, visitor = execute(scriptax)
        assert True
    except:
        assert False


def test_delete_3():
    scriptax = '''
    test = {"day":"night", "up":"down", "yes":"no"};
    del(test);
    '''
    try:
        block_status, visitor = execute(scriptax)
        assert True
    except:
        assert False


def test_delete_4():
    scriptax = '''
    test = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10];
    del(test.5);
    return test;
    '''
    try:
        block_status, visitor = execute(scriptax)
        assert block_status.result == [0, 1, 2, 3, 4, 6, 7, 8, 9, 10]
    except:
        assert False


def test_delete_5():
    scriptax = '''
    test = {"day":"night", "up":"down", "yes":"no"};
    del(test.up);
    return test;
    '''
    try:
        block_status, visitor = execute(scriptax)
        assert block_status.result == {"day": "night", "yes": "no"}
    except:
        assert False