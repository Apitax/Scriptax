from scriptax.tests.pre_test import execute


def test_injection():
    scriptax = '''
    inject = "worked";
    return "<|inject>";
    '''
    block_status, visitor = execute(scriptax)
    assert block_status.result == "worked"


def test_injection_2():
    scriptax = '''
    inject = "worked";
    return "   <|   inject         >     ";
    '''
    block_status, visitor = execute(scriptax)
    assert block_status.result == "   worked     "


def test_injection_3():
    scriptax = '''
    inject = "worked";
    return "hi the  test   <|   inject         >     !";
    '''
    block_status, visitor = execute(scriptax)
    assert block_status.result == "hi the  test   worked     !"


def test_injection_4():
    scriptax = '''
    inject = 42;
    return "hi the  test   <|   inject         >     !";
    '''
    block_status, visitor = execute(scriptax)
    assert block_status.result == "hi the  test   42     !"


def test_injection_5():
    scriptax = '''
    inject = true;
    return "hi the  test   <|   inject         >     !";
    '''
    block_status, visitor = execute(scriptax)
    assert block_status.result == "hi the  test   True     !"


def test_injection_6():
    scriptax = '''
    inject = 0xabcdef1234567890;
    return "hi the  test   <|   inject         >     !";
    '''
    block_status, visitor = execute(scriptax)
    assert block_status.result == "hi the  test   0xABCDEF1234567890     !"


def test_injection_7():
    scriptax = '''
    inject = null;
    return "hi the  test   <|   inject         >     !";
    '''
    block_status, visitor = execute(scriptax)
    assert block_status.result == "hi the  test   None     !"


def test_injection_8():
    scriptax = '''
    mylist = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10];
    inject = 5;
    return mylist.<|inject>;
    '''
    block_status, visitor = execute(scriptax)
    assert block_status.result == 5


def test_injection_9():
    scriptax = '''
    test = {"test": "worked", "test2": [{"yes": "no"}, {"day": "night"}, {"weekend": ["sunday", {"name": "saturday", "best_day": true}]}]};
    inject=["test", "test2", "2", "weekend", "1", "best_day"];
    return <|inject.0>.test2.2.weekend.1.best_day;
    '''
    block_status, visitor = execute(scriptax)
    assert block_status.result == True


def test_injection_10():
    scriptax = '''
    test = {"test": "worked", "test2": [{"yes": "no"}, {"day": "night"}, {"weekend": ["sunday", {"name": "saturday", "best_day": true}]}]};
    inject=["test", "test2", "2", "weekend", "1", "best_day"];
    return <|inject.0>.test2.2.weekend.1.<|inject.5>;
    '''
    block_status, visitor = execute(scriptax)
    assert block_status.result == True


def test_injection_11():
    scriptax = '''
    test = {"test": "worked", "test2": [{"yes": "no"}, {"day": "night"}, {"weekend": ["sunday", {"name": "saturday", "best_day": true}]}]};
    inject=["test", "test2", "2", "weekend", "1", "best_day"];
    return <|inject.0>.<|inject.1>.<|inject.2>.<|inject.3>.<|inject.4>.<|inject.5>;
    '''
    block_status, visitor = execute(scriptax)
    assert block_status.result == True


def test_injection_12():
    scriptax = '''
    test = {"test": "worked", "test2": [{"yes": "no"}, {"day": "night"}, {"weekend": ["sunday", {"name": "saturday", "best_day": true}]}]};
    inject=["test.test2", "2", "weekend", "1", "best_day"];
    return <|inject.0>.<|inject.1>.<|inject.2>.<|inject.3>.<|inject.4>;
    '''
    block_status, visitor = execute(scriptax)
    assert block_status.result == True
