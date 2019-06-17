from scriptax.tests.pre_test import execute


def test_cast_int():
    scriptax = '''
    test = "5";
    return int(test);
    '''
    block_status, visitor = execute(scriptax)
    assert block_status.result == 5


def test_cast_int_2():
    scriptax = '''
    test = "5.4";
    return int(test);
    '''
    block_status, visitor = execute(scriptax)
    assert block_status.result == 5


def test_cast_int_3():
    scriptax = '''
    test = "5.8";
    return int(test);
    '''
    block_status, visitor = execute(scriptax)
    assert block_status.result == 5


def test_cast_dec():
    scriptax = '''
    test = "5";
    return dec(test);
    '''
    block_status, visitor = execute(scriptax)
    assert block_status.result == 5


def test_cast_dec_2():
    scriptax = '''
    test = "5.4";
    return dec(test);
    '''
    block_status, visitor = execute(scriptax)
    assert block_status.result == 5.4


def test_cast_dec_3():
    scriptax = '''
    test = "5.8";
    return dec(test);
    '''
    block_status, visitor = execute(scriptax)
    assert block_status.result == 5.8


def test_cast_bool():
    scriptax = '''
    test = 1;
    return bool(test);
    '''
    block_status, visitor = execute(scriptax)
    assert block_status.result == True


def test_cast_bool_2():
    scriptax = '''
    test = 0;
    return bool(test);
    '''
    block_status, visitor = execute(scriptax)
    assert block_status.result == False


def test_cast_bool_3():
    scriptax = '''
    test = 5.8;
    return bool(test);
    '''
    block_status, visitor = execute(scriptax)
    assert block_status.result == True


def test_cast_bool_4():
    scriptax = '''
    test = -5.8;
    return bool(test);
    '''
    block_status, visitor = execute(scriptax)
    assert block_status.result == True


def test_cast_bool_5():
    scriptax = '''
    test = "true";
    return bool(test);
    '''
    block_status, visitor = execute(scriptax)
    assert block_status.result == True


def test_cast_bool_6():
    scriptax = '''
    test = "True";
    return bool(test);
    '''
    block_status, visitor = execute(scriptax)
    assert block_status.result == True


def test_cast_bool_7():
    scriptax = '''
    test = "false";
    return bool(test);
    '''
    block_status, visitor = execute(scriptax)
    assert block_status.result == False


def test_cast_bool_8():
    scriptax = '''
    test = "False";
    return bool(test);
    '''
    block_status, visitor = execute(scriptax)
    assert block_status.result == False


def test_cast_bool_9():
    scriptax = '''
    test = "";
    return bool(test);
    '''
    block_status, visitor = execute(scriptax)
    assert block_status.result == False


def test_cast_string():
    scriptax = '''
    test = 0;
    return str(test);
    '''
    block_status, visitor = execute(scriptax)
    assert block_status.result == "0"


def test_cast_string_2():
    scriptax = '''
    test = -5.6987;
    return str(test);
    '''
    block_status, visitor = execute(scriptax)
    assert block_status.result == "-5.6987"


def test_cast_string_3():
    scriptax = '''
    test = 96766744532;
    return str(test);
    '''
    block_status, visitor = execute(scriptax)
    assert block_status.result == "96766744532"


def test_cast_string_4():
    scriptax = '''
    test = true;
    return str(test);
    '''
    block_status, visitor = execute(scriptax)
    assert block_status.result == "True"


def test_cast_string_5():
    scriptax = '''
    test = false;
    return str(test);
    '''
    block_status, visitor = execute(scriptax)
    assert block_status.result == "False"


def test_cast_string_6():
    scriptax = '''
    test = null;
    return str(test);
    '''
    block_status, visitor = execute(scriptax)
    assert block_status.result == "None"


def test_cast_list():
    scriptax = '''
    test = "0,1,2,3,4,5,6,7,8,9,10";
    return list(test);
    '''
    block_status, visitor = execute(scriptax)
    assert block_status.result == ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10']


def test_cast_list_2():
    scriptax = '''
    test = "";
    return list(test);
    '''
    block_status, visitor = execute(scriptax)
    assert block_status.result == [""]


def test_cast_dict():
    scriptax = '''
    test = {"yes": "no", "weekend": ["saturday", {"sunday": "icecream"}]};
    return dict(test);
    '''
    block_status, visitor = execute(scriptax)
    assert block_status.result == {"yes": "no", "weekend": ["saturday", {"sunday": "icecream"}]}


def test_cast_dict_2():
    scriptax = '''
    test = [{"yes": "no", "weekend": ["saturday", {"sunday": "icecream"}]}];
    return dict(test);
    '''
    block_status, visitor = execute(scriptax)
    assert block_status.result == {"0": {"yes": "no", "weekend": ["saturday", {"sunday": "icecream"}]}}


def test_cast_dict_3():
    scriptax = '''
    test = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10];
    return dict(test);
    '''
    block_status, visitor = execute(scriptax)
    assert block_status.result == {"0": 0, "1": 1, "2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "8": 8, "9": 9,
                                   "10": 10}


def test_cast_dict_4():
    scriptax = '''
    test = '{"day": "night", "nottrue": false}';
    return dict(test);
    '''
    block_status, visitor = execute(scriptax)
    assert block_status.result == {"day": "night", "nottrue": False}


def test_cast_dict_5():
    scriptax = '''
    test = "test";
    return dict(test);
    '''
    block_status, visitor = execute(scriptax)
    assert block_status.result == {"default": "test"}


def test_cast_dict_6():
    scriptax = '''
    test = 85;
    return dict(test);
    '''
    block_status, visitor = execute(scriptax)
    assert block_status.result == {"default": 85}


def test_cast_dict_7():
    scriptax = '''
    test = true;
    return dict(test);
    '''
    block_status, visitor = execute(scriptax)
    assert block_status.result == {"default": True}


def test_cast_dict_8():
    scriptax = '''
    test = null;
    return dict(test);
    '''
    block_status, visitor = execute(scriptax)
    assert block_status.result == {"default": None}