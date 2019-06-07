from scriptax.tests.pre_test import execute


def test_for():
    scriptax = '''
    test = 0;
    for i in 10 {
        test = i;
    }
    return test;
    '''
    block_status, visitor = execute(scriptax)
    assert block_status.result == 9


def test_for_2():
    scriptax = '''
    test = 0;
    for i in 10 {
        if(i > 5)
        {
            continue;
        }
        test = i;
    }
    return test;
    '''
    block_status, visitor = execute(scriptax)
    assert block_status.result == 5


def test_for_3():
    scriptax = '''
    test = 0;
    for i in 10 {
        if(i > 5)
        {
            return 3;
        }
        test = i;
    }
    return test;
    '''
    block_status, visitor = execute(scriptax)
    assert block_status.result == 3


def test_for_4():
    scriptax = '''
    test = 0;
    for i in 10 {
        if(i == 5)
        {
            done;
        }
        test++;
    }
    return test;
    '''
    block_status, visitor = execute(scriptax)
    assert block_status.result == 5


def test_for_5():
    scriptax = '''
    test = 0;
    for i in 10 {
        if(i == 5)
        {
            continue;
        }
        test++;
    }
    return test;
    '''
    block_status, visitor = execute(scriptax)
    assert block_status.result == 9


def test_for_6():
    scriptax = '''
    test = 0;
    for i in 10 {
        test++;
    }
    return test;
    '''
    block_status, visitor = execute(scriptax)
    assert block_status.result == 10


def test_for_7():
    scriptax = '''
    test = 0;
    for i in [] {
        test += i;
    }
    return test;
    '''
    block_status, visitor = execute(scriptax)
    assert block_status.result == 0


def test_for_8():
    scriptax = '''
    test = 0;
    for i in [1, 2, 5] {
        test += i;
    }
    return test;
    '''
    block_status, visitor = execute(scriptax)
    assert block_status.result == 8


def test_for_9():
    scriptax = '''
    test = 0;
    for i in [1, 2, 5] {
        if(i == 2)
            return i;
    }
    return test;
    '''
    block_status, visitor = execute(scriptax)
    assert block_status.result == 2


def test_for_10():
    scriptax = '''
    test = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10];
    worked = [];
    for i in test {
        if(i < 10)
            worked[] = i;
    }
    return worked;
    '''
    block_status, visitor = execute(scriptax)
    assert block_status.result == [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]


def test_for_11():
    scriptax = '''
    test = [{'well': false, "id": 0}, {'well': true, 'id': 1}, {'well': false, 'id': 2}, {'well': true, 'id': 3}];
    worked = [];
    for i in test
        if(i.well)
            worked[] = i;
    return worked;
    '''
    block_status, visitor = execute(scriptax)
    assert block_status.result == [{'well': True, 'id': 1}, {'well': True, 'id': 3}]