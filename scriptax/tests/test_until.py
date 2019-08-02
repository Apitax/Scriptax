from scriptax.tests.pre_test import execute


def test_until():
    scriptax = '''
    test = 0;
    until test==10 {
        test++;
    }
    return test;
    '''
    block_status, visitor = execute(scriptax)
    assert block_status.result == 10


def test_until_2():
    scriptax = '''
    test = 0;
    until (test==10) {
        test++;
    }
    return test;
    '''
    block_status, visitor = execute(scriptax)
    assert block_status.result == 10


def test_until_3():
    scriptax = '''
    test = 0;
    until test==10, -1 {
        test++;
    }
    return test;
    '''
    block_status, visitor = execute(scriptax)
    assert block_status.result == 10


def test_until_4():
    scriptax = '''
    test = 0;
    until test==10, 0 {
        test++;
    }
    return test;
    '''
    block_status, visitor = execute(scriptax)
    assert block_status.result == 0


def test_until_5():
    scriptax = '''
    test = 0;
    until test==10, 5 {
        test++;
    }
    return test;
    '''
    block_status, visitor = execute(scriptax)
    assert block_status.result == 5


def test_until_6():
    scriptax = '''
    test = 0;
    until test==10, 5, 200 {
        test++;
    }
    return test;
    '''
    block_status, visitor = execute(scriptax)
    assert block_status.result == 5
