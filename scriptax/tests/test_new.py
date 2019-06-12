from scriptax.tests.pre_test import execute


def test_new():
    scriptax = '''
    from scriptax import testing;
    test = new testing();
    return true;
    '''
    block_status, visitor = execute(scriptax)
    assert block_status.result == True


def test_new_2():
    scriptax = '''
    from scriptax import testing;
    test = new testing();
    return test.get_test();
    '''
    block_status, visitor = execute(scriptax)
    assert block_status.result == "worked"


def test_new_3():
    scriptax = '''
    from scriptax import testing;
    test = new testing();
    return test.get_advanced_test();
    '''
    block_status, visitor = execute(scriptax)
    assert block_status.result == "worked worked worked."


def test_new_4():
    scriptax = '''
    from scriptax import testing;
    test = new testing();
    return test.test;
    '''
    block_status, visitor = execute(scriptax)
    assert block_status.result == "worked"


def test_new_5():
    scriptax = '''
    from scriptax import testing;
    test = new testing();
    return test.worked;
    '''
    block_status, visitor = execute(scriptax)
    assert block_status.result == "test"


def test_new_6():
    scriptax = '''
    from scriptax import advanced_testing as testing;
    test = new testing();
    return test.worked;
    '''
    block_status, visitor = execute(scriptax)
    assert block_status.result == "test worked"


def test_new_7():
    scriptax = '''
    from scriptax import advanced_testing as testing;
    test = new testing(param="worked for sure.");
    return test.worked;
    '''
    block_status, visitor = execute(scriptax)
    assert block_status.result == "test worked for sure."



