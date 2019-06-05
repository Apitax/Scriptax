from scriptax.tests.pre_test import execute


def test_enum():
    scriptax = '''
    test = ();
    return test;
    '''
    block_status, visitor = execute(scriptax)
    assert block_status.result == {}


def test_enum_2():
    scriptax = '''
    test = (Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday);
    return test;
    '''
    block_status, visitor = execute(scriptax)
    assert block_status.result == {"Monday": 0, "Tuesday": 1, "Wednesday": 2, "Thursday": 3, "Friday": 4, "Saturday": 5,
                                   "Sunday": 6}


def test_enum_3():
    scriptax = '''
    test = (Monday -> 42, Tuesday -> 84, Wednesday -> 126);
    return test;
    '''
    block_status, visitor = execute(scriptax)
    assert block_status.result == {"Monday": 42, "Tuesday": 84, "Wednesday": 126}


def test_enum_4():
    scriptax = '''
    worked = "test";
    test = (Monday -> 42, Tuesday -> worked, Wednesday -> 126);
    return test;
    '''
    block_status, visitor = execute(scriptax)
    assert block_status.result == {"Monday": 42, "Tuesday": "test", "Wednesday": 126}


def test_enum_5():
    scriptax = '''
    worked = "test";
    test = (Monday -> 42, Tuesday -> worked, Wednesday -> 126);
    return test.Tuesday;
    '''
    block_status, visitor = execute(scriptax)
    assert block_status.result == "test"


def test_enum_6():
    scriptax = '''
    worked = "test";
    test = (Monday -> 42, Tuesday -> worked, Wednesday -> 126);
    return test.Wednesday;
    '''
    block_status, visitor = execute(scriptax)
    assert block_status.result == 126


def test_enum_7():
    scriptax = '''
    test = (Monday -> 42, Tuesday -> 42, Wednesday -> 126);
    return test.Monday == test.Monday;
    '''
    block_status, visitor = execute(scriptax)
    assert block_status.result == True


def test_enum_8():
    scriptax = '''
    test = (Monday -> 42, Tuesday -> 42, Wednesday -> 126);
    return test.Monday == test.Tuesday;
    '''
    block_status, visitor = execute(scriptax)
    assert block_status.result == True


def test_enum_9():
    scriptax = '''
    test = (Monday -> 42, Tuesday -> 42, Wednesday -> 126);
    return test.Wednesday == test.Monday;
    '''
    block_status, visitor = execute(scriptax)
    assert block_status.result == False


def test_enum_10():
    scriptax = '''
    test = (Monday, Tuesday, Wednesday);
    return test.Wednesday == test.Monday;
    '''
    block_status, visitor = execute(scriptax)
    assert block_status.result == False


def test_enum_11():
    scriptax = '''
    test = (Monday, Tuesday, Wednesday);
    return test.Monday == test.Monday;
    '''
    block_status, visitor = execute(scriptax)
    assert block_status.result == True