from apitaxcore.logs.Log import Log
from apitaxcore.logs.StandardLog import StandardLog
from apitaxcore.models.State import State
from apitaxcore.models.Options import Options
from apitaxcore.flow.LoadedDrivers import LoadedDrivers
from apitaxcore.drivers.Drivers import Drivers
from scriptax.parser.utils.BoilerPlate import customizable_parser, read_string
from scriptax.drivers.builtin.Scriptax import Scriptax
from scriptax.models.BlockStatus import BlockStatus
from typing import Tuple, Any
from scriptax.parser.Visitor import AhVisitor

State.log = Log(StandardLog(), logColorize=False)
State.log.log("")
State.log.log("> Running test_language.py\n\n")

Drivers.add("scriptax", Scriptax())
LoadedDrivers.load("scriptax")


def execute(scriptax: str) -> Tuple[BlockStatus, AhVisitor]:
    return customizable_parser(read_string(scriptax), file='inline_program', options=Options(debug=True))


def test_return():
    scriptax = '''
    return "test";
    '''
    block_status, visitor = execute(scriptax)
    assert block_status.result == "test"


def test_int():
    scriptax = '''
    test = 5;
    return test;
    '''
    block_status, visitor = execute(scriptax)
    assert block_status.result == 5


def test_negative_int():
    scriptax = '''
    test = -509;
    return test;
    '''
    block_status, visitor = execute(scriptax)
    assert block_status.result == -509


def test_big_int():
    scriptax = '''
    test = 5099327593287521432626;
    return test;
    '''
    block_status, visitor = execute(scriptax)
    assert block_status.result == 5099327593287521432626


def test_float():
    scriptax = '''
    test = 5.59087765554444111;
    return test;
    '''
    block_status, visitor = execute(scriptax)
    assert block_status.result == 5.59087765554444111


def test_string():
    scriptax = '''
    test = "what's my name !@#$%^&*()-=_+[]{}|;':,./<>?\'\\";
    return test;
    '''
    block_status, visitor = execute(scriptax)
    assert block_status.result == "what's my name !@#$%^&*()-=_+[]{}|;':,./<>?\'\\"


def test_boolean():
    scriptax = '''
    test = true;
    return test;
    '''
    block_status, visitor = execute(scriptax)
    assert block_status.result == True


def test_boolean2():
    scriptax = '''
    test = false;
    return test;
    '''
    block_status, visitor = execute(scriptax)
    assert block_status.result == False


def test_none():
    scriptax = '''
    test = null;
    return test;
    '''
    block_status, visitor = execute(scriptax)
    assert block_status.result == None


def test_hex():
    scriptax = '''
    test = 0xabcdEF1234567890;
    return test;
    '''
    block_status, visitor = execute(scriptax)
    assert block_status.result == "0xABCDEF1234567890"


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


def test_label_escaping():
    scriptax = '''
    $test = "worked";
    return $test;
    '''
    block_status, visitor = execute(scriptax)
    assert block_status.result == "worked"


def test_label_escaping_2():
    scriptax = '''
    $test = "worked";
    return test;
    '''
    block_status, visitor = execute(scriptax)
    assert block_status.result == "worked"


def test_label_escaping_3():
    scriptax = '''
    $for = "worked";
    return $for;
    '''
    block_status, visitor = execute(scriptax)
    assert block_status.result == "worked"


def test_label_escaping_4():
    scriptax = '''
    $return = "worked";
    return $return;
    '''
    block_status, visitor = execute(scriptax)
    assert block_status.result == "worked"


def test_label_escaping_5():
    scriptax = '''
    $return = {"return": "worked"};
    return $return.$return;
    '''
    block_status, visitor = execute(scriptax)
    assert block_status.result == "worked"