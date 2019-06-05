from scriptax.tests.pre_test import execute


def test_dict():
    scriptax = '''
    test = {"test": "worked"};
    return test;
    '''
    block_status, visitor = execute(scriptax)
    assert block_status.result == {"test": "worked"}


def test_dict_2():
    scriptax = '''
    test = {"test": "worked", "test2": -509, "test3": 931523298765, "test4": null, "test5": 0xabcdef1234567890, "test6": true, "test7": false};
    return test;
    '''
    block_status, visitor = execute(scriptax)
    assert block_status.result == {"test": "worked", "test2": -509, "test3": 931523298765, "test4": None,
                                   "test5": "0xABCDEF1234567890", "test6": True, "test7": False}


def test_dict_access():
    scriptax = '''
    test = {"test": "worked"};
    return test.test;
    '''
    block_status, visitor = execute(scriptax)
    assert block_status.result == "worked"


def test_dict_access_2():
    scriptax = '''
    test = {"test_test": "worked"};
    return test.test_test;
    '''
    block_status, visitor = execute(scriptax)
    assert block_status.result == "worked"


def test_dict_access_3():
    scriptax = '''
    test = {"5": "worked"};
    return test.5;
    '''
    block_status, visitor = execute(scriptax)
    assert block_status.result == "worked"


def test_complex_object():
    scriptax = '''
    test = {"test": "worked", "test2": [{"yes": "no"}, {"day": "night"}, {"weekend": ["sunday", {"name": "saturday", "best_day": true}]}]};
    return test.test2.2.weekend.1.best_day;
    '''
    block_status, visitor = execute(scriptax)
    assert block_status.result == True