from scriptax.tests.pre_test import execute


def test_count():
    scriptax = '''
    test = "hi my name is test";
    return #test;
    '''
    block_status, visitor = execute(scriptax)
    assert block_status.result == 18


def test_count_2():
    scriptax = '''
    test = "";
    return #test;
    '''
    block_status, visitor = execute(scriptax)
    assert block_status.result == 0


def test_count_3():
    scriptax = '''
    test = [0,1,2,3,4,5,6,7,8,9,10];
    return #test;
    '''
    block_status, visitor = execute(scriptax)
    assert block_status.result == 11


def test_count_4():
    scriptax = '''
    test = [];
    return #test;
    '''
    block_status, visitor = execute(scriptax)
    assert block_status.result == 0


def test_count_5():
    scriptax = '''
    test = {"up":"down", "yes":"no"};
    return #test;
    '''
    block_status, visitor = execute(scriptax)
    assert block_status.result == 2


def test_count_6():
    scriptax = '''
    test = {};
    return #test;
    '''
    block_status, visitor = execute(scriptax)
    assert block_status.result == 0
