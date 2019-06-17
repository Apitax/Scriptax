from scriptax.tests.pre_test import execute


def test_if():
    scriptax = '''
    test = true;
    if(test)
    {
        test = false;
    } else if(!test) {
        test = "didnt work";
    } else {
        test = "definitely did not work";
    }
    return test;
    '''
    block_status, visitor = execute(scriptax)
    assert block_status.result == False


def test_if_2():
    scriptax = '''
    test = false;
    if(test)
    {
        test = false;
    } else if(!test) {
        test = "worked";
    } else {
        test = "definitely did not work";
    }
    return test;
    '''
    block_status, visitor = execute(scriptax)
    assert block_status.result == "worked"


def test_if_3():
    scriptax = '''
    test = "test";
    if(test == 5)
    {
        test = false;
    } else if(!test) {
        test = "didnt work";
    } else {
        test = "worked";
    }
    return test;
    '''
    block_status, visitor = execute(scriptax)
    assert block_status.result == "worked"


def test_if_4():
    scriptax = '''
    test = 0xabcdef1234567890;
    if(test == 0xabcdef1234567890)
    {
        test = true;
    } else {
        test = false;
    }
    return test;
    '''
    block_status, visitor = execute(scriptax)
    assert block_status.result == True


def test_if_5():
    scriptax = '''
    test = 0xabcdef1234567890;
    if(test == 0xaacdef1234567890)
    {
        test = true;
    } else {
        test = false;
    }
    return test;
    '''
    block_status, visitor = execute(scriptax)
    assert block_status.result == False


def test_if_6():
    scriptax = '''
    test = null;
    if(test == null)
    {
        test = true;
    } else {
        test = false;
    }
    return test;
    '''
    block_status, visitor = execute(scriptax)
    assert block_status.result == True


def test_if_7():
    scriptax = '''
    test = 'test';
    if(test == null)
    {
        test = true;
    } else {
        test = false;
    }
    return test;
    '''
    block_status, visitor = execute(scriptax)
    assert block_status.result == False


def test_if_8():
    scriptax = '''
    test = [1,2,3,4,5,6,7,8,9,10];
    if(test == [1,2,3,4,5,6,7,8,9,10])
    {
        test = true;
    } else {
        test = false;
    }
    return test;
    '''
    block_status, visitor = execute(scriptax)
    assert block_status.result == True


def test_if_9():
    scriptax = '''
    test = [1,2,3,4,5,6,7,8,9,10];
    if(test == [1,2,3,4,5,6,7,7,9,10])
    {
        test = true;
    } else {
        test = false;
    }
    return test;
    '''
    block_status, visitor = execute(scriptax)
    assert block_status.result == False


def test_if_10():
    scriptax = '''
    test = [{"test":"worked"}, {"yes":"no"}];
    if(test == [{"test":"worked"}, {"yes":"no"}])
    {
        test = true;
    } else {
        test = false;
    }
    return test;
    '''
    block_status, visitor = execute(scriptax)
    assert block_status.result == True


def test_if_11():
    scriptax = '''
    test = [{"test":"worked"}, {"yes":"no"}];
    if(test == [{"test":"worked"}, {"yes":"nope"}])
    {
        test = true;
    } else {
        test = false;
    }
    return test;
    '''
    block_status, visitor = execute(scriptax)
    assert block_status.result == False


def test_if_12():
    scriptax = '''
    test = (YES, NOPE, MAYBE_SO);
    choice = test.YES;
    if(test.YES == choice)
    {
        test = true;
    } else {
        test = false;
    }
    return test;
    '''
    block_status, visitor = execute(scriptax)
    assert block_status.result == True