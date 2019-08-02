from scriptax.tests.pre_test import execute
from scriptax.exceptions.InvalidType import InvalidType


def test_typing():
    scriptax = '''
    int test = 0;
    test = false;
    return test;
    '''
    try:
        block_status, visitor = execute(scriptax)
        assert False
    except InvalidType:
        assert True


def test_typing_2():
    scriptax = '''
    any test = 0;
    test = false;
    return test;
    '''
    try:
        block_status, visitor = execute(scriptax)
        assert block_status.result == False
    except InvalidType:
        assert False


def test_typing_3():
    scriptax = '''
    dec test = 0.678;
    test = false;
    return test;
    '''
    try:
        block_status, visitor = execute(scriptax)
        assert False
    except InvalidType:
        assert True


def test_typing_4():
    scriptax = '''
    bool test = false;
    test = 3;
    return test;
    '''
    try:
        block_status, visitor = execute(scriptax)
        assert False
    except InvalidType:
        assert True

def test_typing_5():
    scriptax = '''
    dict test = {'day': ['night']};
    test = false;
    return test;
    '''
    try:
        block_status, visitor = execute(scriptax)
        assert False
    except InvalidType:
        assert True


def test_typing_6():
    scriptax = '''
    hex test = 0x0123456789abcdef;
    test = false;
    return test;
    '''
    try:
        block_status, visitor = execute(scriptax)
        assert False
    except InvalidType:
        assert True


def test_typing_7():
    scriptax = '''
    list test = [0,1,2,3,4,5,6,7,8,9];
    test = false;
    return test;
    '''
    try:
        block_status, visitor = execute(scriptax)
        assert False
    except InvalidType:
        assert True


def test_typing_8():
    scriptax = '''
    method test = () -> {};
    test = false;
    return test;
    '''
    try:
        block_status, visitor = execute(scriptax)
        assert False
    except InvalidType:
        assert True


def test_typing_9():
    scriptax = '''
    none test = null;
    test = false;
    return test;
    '''
    try:
        block_status, visitor = execute(scriptax)
        assert False
    except InvalidType:
        assert True


def test_typing_10():
    scriptax = '''
    str test = "test";
    test = "okay";
    return test;
    '''
    try:
        block_status, visitor = execute(scriptax)
        assert block_status.result == "okay"
    except InvalidType:
        assert False


def test_typing_11():
    scriptax = '''
    int test = 0;
    test = 50;
    return test;
    '''
    try:
        block_status, visitor = execute(scriptax)
        assert block_status.result == 50
    except InvalidType:
        assert False


def test_typing_12():
    scriptax = '''
    any test = 0;
    test = "cheese";
    return test;
    '''
    try:
        block_status, visitor = execute(scriptax)
        assert block_status.result == "cheese"
    except InvalidType:
        assert False


def test_typing_13():
    scriptax = '''
    dec test = 0.678;
    test = 3.14159;
    return test;
    '''
    try:
        block_status, visitor = execute(scriptax)
        assert block_status.result == 3.14159
    except InvalidType:
        assert False


def test_typing_14():
    scriptax = '''
    bool test = false;
    test = true;
    return test;
    '''
    try:
        block_status, visitor = execute(scriptax)
        assert block_status.result == True
    except InvalidType:
        assert False

def test_typing_15():
    scriptax = '''
    dict test = {'day': ['night']};
    test = {'night': ['day']};
    return test;
    '''
    try:
        block_status, visitor = execute(scriptax)
        assert block_status.result == {'night': ['day']}
    except InvalidType:
        assert False


def test_typing_16():
    scriptax = '''
    hex test = 0x0123456789abcdef;
    test = 0xabcdef0123456789;
    return test;
    '''
    try:
        block_status, visitor = execute(scriptax)
        assert block_status.result == "0xABCDEF0123456789"
    except InvalidType:
        assert False


def test_typing_17():
    scriptax = '''
    list test = [0,1,2,3,4,5,6,7,8,9];
    test = [9,8,7,6,5,4,3,2,1,0];
    return test;
    '''
    try:
        block_status, visitor = execute(scriptax)
        assert block_status.result == [9,8,7,6,5,4,3,2,1,0]
    except InvalidType:
        assert False


def test_typing_18():
    scriptax = '''
    pythonic test = () -> {};
    test = () -> {return "worked";};
    return test();
    '''
    try:
        block_status, visitor = execute(scriptax)
        assert block_status.result == "worked"
    except InvalidType:
        assert False


def test_typing_19():
    scriptax = '''
    none test = null;
    test = none;
    return test;
    '''
    try:
        block_status, visitor = execute(scriptax)
        assert block_status.result == None
    except InvalidType:
        assert False


def test_typing_20():
    scriptax = '''
    str test = "test";
    test = "worked";
    return test;
    '''
    try:
        block_status, visitor = execute(scriptax)
        assert block_status.result == "worked"
    except InvalidType:
        assert False

def test_typing_21():
    scriptax = '''
    int test = false;
    return test;
    '''
    try:
        block_status, visitor = execute(scriptax)
        assert False
    except InvalidType:
        assert True


def test_typing_22():
    scriptax = '''
    any test = false;
    return test;
    '''
    try:
        block_status, visitor = execute(scriptax)
        assert block_status.result == False
    except InvalidType:
        assert False


def test_typing_23():
    scriptax = '''
    dec test = false;
    return test;
    '''
    try:
        block_status, visitor = execute(scriptax)
        assert False
    except InvalidType:
        assert True


def test_typing_24():
    scriptax = '''
    bool test = 3;
    return test;
    '''
    try:
        block_status, visitor = execute(scriptax)
        assert False
    except InvalidType:
        assert True

def test_typing_25():
    scriptax = '''
    dict test = false;
    return test;
    '''
    try:
        block_status, visitor = execute(scriptax)
        assert False
    except InvalidType:
        assert True


def test_typing_26():
    scriptax = '''
    hex test = false;
    return test;
    '''
    try:
        block_status, visitor = execute(scriptax)
        assert False
    except InvalidType:
        assert True


def test_typing_27():
    scriptax = '''
    list test = false;
    return test;
    '''
    try:
        block_status, visitor = execute(scriptax)
        assert False
    except InvalidType:
        assert True


def test_typing_28():
    scriptax = '''
    method test = false;
    return test;
    '''
    try:
        block_status, visitor = execute(scriptax)
        assert False
    except InvalidType:
        assert True


def test_typing_29():
    scriptax = '''
    none test = "worked";
    return test;
    '''
    try:
        block_status, visitor = execute(scriptax)
        assert False
    except InvalidType:
        assert True


def test_typing_30():
    scriptax = '''
    str test = false;
    return test;
    '''
    try:
        block_status, visitor = execute(scriptax)
        assert False
    except InvalidType:
        assert True


def test_typing_31():
    scriptax = '''
    script any test(int param)
    {
        return param;
    }
    return test(param=false);
    '''
    try:
        block_status, visitor = execute(scriptax)
        assert False
    except InvalidType:
        assert True


def test_typing_32():
    scriptax = '''
    script any test(any param)
    {
        return param;
    }
    return test(param=false);
    '''
    try:
        block_status, visitor = execute(scriptax)
        assert block_status.result == False
    except InvalidType:
        assert False


def test_typing_33():
    scriptax = '''
    script any test(dec param)
    {
        return param;
    }
    return test(param=false);
    '''
    try:
        block_status, visitor = execute(scriptax)
        assert False
    except InvalidType:
        assert True


def test_typing_34():
    scriptax = '''
    script any test(bool param)
    {
        return param;
    }
    return test(param=3);
    '''
    try:
        block_status, visitor = execute(scriptax)
        assert False
    except InvalidType:
        assert True

def test_typing_35():
    scriptax = '''
    script any test(dict param)
    {
        return param;
    }
    return test(param=false);
    '''
    try:
        block_status, visitor = execute(scriptax)
        assert False
    except InvalidType:
        assert True


def test_typing_36():
    scriptax = '''
    script any test(hex param)
    {
        return param;
    }
    return test(param=false);
    '''
    try:
        block_status, visitor = execute(scriptax)
        assert False
    except InvalidType:
        assert True


def test_typing_37():
    scriptax = '''
    script any test(list param)
    {
        return param;
    }
    return test(param=false);
    '''
    try:
        block_status, visitor = execute(scriptax)
        assert False
    except InvalidType:
        assert True


def test_typing_38():
    scriptax = '''
    script any test(method param)
    {
        return param;
    }
    return test(param=false);
    '''
    try:
        block_status, visitor = execute(scriptax)
        assert False
    except InvalidType:
        assert True


def test_typing_39():
    scriptax = '''
    script any test(none param)
    {
        return param;
    }
    return test(param=false);
    '''
    try:
        block_status, visitor = execute(scriptax)
        assert False
    except InvalidType:
        assert True


def test_typing_40():
    scriptax = '''
    script any test(str param)
    {
        return param;
    }
    return test(param=false);
    '''
    try:
        block_status, visitor = execute(scriptax)
        assert False
    except InvalidType:
        assert True


def test_typing_41():
    scriptax = '''
    script any test(int param)
    {
        return param;
    }
    return test(param=3);
    '''
    try:
        block_status, visitor = execute(scriptax)
        assert block_status.result == 3
    except InvalidType:
        assert False


def test_typing_42():
    scriptax = '''
    script any test(any param)
    {
        return param;
    }
    return test(param=false);
    '''
    try:
        block_status, visitor = execute(scriptax)
        assert block_status.result == False
    except InvalidType:
        assert False


def test_typing_43():
    scriptax = '''
    script any test(dec param)
    {
        return param;
    }
    return test(param=3.14159);
    '''
    try:
        block_status, visitor = execute(scriptax)
        assert block_status.result == 3.14159
    except InvalidType:
        assert False


def test_typing_44():
    scriptax = '''
    script any test(bool param)
    {
        return param;
    }
    return test(param=True);
    '''
    try:
        block_status, visitor = execute(scriptax)
        assert block_status.result == True
    except InvalidType:
        assert False

def test_typing_45():
    scriptax = '''
    script any test(dict param)
    {
        return param;
    }
    return test(param={'day': ['night']});
    '''
    try:
        block_status, visitor = execute(scriptax)
        assert block_status.result == {'day': ['night']}
    except InvalidType:
        assert False


def test_typing_46():
    scriptax = '''
    script any test(hex param)
    {
        return param;
    }
    return test(param=0x0123456789abcdef);
    '''
    try:
        block_status, visitor = execute(scriptax)
        assert block_status.result == "0x0123456789ABCDEF"
    except InvalidType:
        assert False


def test_typing_47():
    scriptax = '''
    script any test(list param)
    {
        return param;
    }
    return test(param=[0,1,2,3,4,5,6,7,8,9]);
    '''
    try:
        block_status, visitor = execute(scriptax)
        assert block_status.result == [0,1,2,3,4,5,6,7,8,9]
    except InvalidType:
        assert False


def test_typing_48():
    scriptax = '''
    script any test(pythonic param)
    {
        return param();
    }
    return test(param=() -> {return "worked";});
    '''
    try:
        block_status, visitor = execute(scriptax)
        assert block_status.result == "worked"
    except InvalidType:
        assert False


def test_typing_49():
    scriptax = '''
    script any test(none param)
    {
        return param;
    }
    return test(param=null);
    '''
    try:
        block_status, visitor = execute(scriptax)
        assert block_status.result == None
    except InvalidType:
        assert False


def test_typing_50():
    scriptax = '''
    script any test(str param)
    {
        return param;
    }
    return test(param="worked");
    '''
    try:
        block_status, visitor = execute(scriptax)
        assert block_status.result == "worked"
    except InvalidType:
        assert False

def test_typing_51():
    scriptax = '''
    script int test(int param)
    {
        return param;
    }
    return test(param=3);
    '''
    try:
        block_status, visitor = execute(scriptax)
        assert block_status.result == 3
    except InvalidType:
        assert False


def test_typing_52():
    scriptax = '''
    script any test(any param)
    {
        return param;
    }
    return test(param=false);
    '''
    try:
        block_status, visitor = execute(scriptax)
        assert block_status.result == False
    except InvalidType:
        assert False


def test_typing_53():
    scriptax = '''
    script dec test(dec param)
    {
        return param;
    }
    return test(param=3.14159);
    '''
    try:
        block_status, visitor = execute(scriptax)
        assert block_status.result == 3.14159
    except InvalidType:
        assert False


def test_typing_54():
    scriptax = '''
    script bool test(bool param)
    {
        return param;
    }
    return test(param=True);
    '''
    try:
        block_status, visitor = execute(scriptax)
        assert block_status.result == True
    except InvalidType:
        assert False

def test_typing_55():
    scriptax = '''
    script dict test(dict param)
    {
        return param;
    }
    return test(param={'day': ['night']});
    '''
    try:
        block_status, visitor = execute(scriptax)
        assert block_status.result == {'day': ['night']}
    except InvalidType:
        assert False


def test_typing_56():
    scriptax = '''
    script hex test(hex param)
    {
        return param;
    }
    return test(param=0x0123456789abcdef);
    '''
    try:
        block_status, visitor = execute(scriptax)
        assert block_status.result == "0x0123456789ABCDEF"
    except InvalidType:
        assert False


def test_typing_57():
    scriptax = '''
    script list test(list param)
    {
        return param;
    }
    return test(param=[0,1,2,3,4,5,6,7,8,9]);
    '''
    try:
        block_status, visitor = execute(scriptax)
        assert block_status.result == [0,1,2,3,4,5,6,7,8,9]
    except InvalidType:
        assert False


def test_typing_58():
    scriptax = '''
    script str test(pythonic param)
    {
        return param();
    }
    return test(param=() -> {return "worked";});
    '''
    try:
        block_status, visitor = execute(scriptax)
        assert block_status.result == "worked"
    except InvalidType:
        assert False


def test_typing_59():
    scriptax = '''
    script none test(none param)
    {
        return param;
    }
    return test(param=null);
    '''
    try:
        block_status, visitor = execute(scriptax)
        assert block_status.result == None
    except InvalidType:
        assert False


def test_typing_60():
    scriptax = '''
    script str test(str param)
    {
        return param;
    }
    return test(param="worked");
    '''
    try:
        block_status, visitor = execute(scriptax)
        assert block_status.result == "worked"
    except InvalidType:
        assert False


def test_typing_61():
    scriptax = '''
    script int test(bool param)
    {
        return param;
    }
    return test(param=false);
    '''
    try:
        block_status, visitor = execute(scriptax)
        assert False
    except InvalidType:
        assert True


def test_typing_62():
    scriptax = '''
    script any test(bool param)
    {
        return param;
    }
    return test(param=false);
    '''
    try:
        block_status, visitor = execute(scriptax)
        assert block_status.result == False
    except InvalidType:
        assert False


def test_typing_63():
    scriptax = '''
    script dec test(bool param)
    {
        return param;
    }
    return test(param=false);
    '''
    try:
        block_status, visitor = execute(scriptax)
        assert False
    except InvalidType:
        assert True


def test_typing_64():
    scriptax = '''
    script bool test(int param)
    {
        return param;
    }
    return test(param=3);
    '''
    try:
        block_status, visitor = execute(scriptax)
        assert False
    except InvalidType:
        assert True

def test_typing_65():
    scriptax = '''
    script dict test(bool param)
    {
        return param;
    }
    return test(param=false);
    '''
    try:
        block_status, visitor = execute(scriptax)
        assert False
    except InvalidType:
        assert True


def test_typing_66():
    scriptax = '''
    script hex test(bool param)
    {
        return param;
    }
    return test(param=false);
    '''
    try:
        block_status, visitor = execute(scriptax)
        assert False
    except InvalidType:
        assert True


def test_typing_67():
    scriptax = '''
    script list test(bool param)
    {
        return param;
    }
    return test(param=false);
    '''
    try:
        block_status, visitor = execute(scriptax)
        assert False
    except InvalidType:
        assert True


def test_typing_68():
    scriptax = '''
    script method test(bool param)
    {
        return param;
    }
    return test(param=false);
    '''
    try:
        block_status, visitor = execute(scriptax)
        assert False
    except InvalidType:
        assert True


def test_typing_69():
    scriptax = '''
    script none test(bool param)
    {
        return param;
    }
    return test(param=false);
    '''
    try:
        block_status, visitor = execute(scriptax)
        assert False
    except InvalidType:
        assert True


def test_typing_70():
    scriptax = '''
    script str test(bool param)
    {
        return param;
    }
    return test(param=false);
    '''
    try:
        block_status, visitor = execute(scriptax)
        assert False
    except InvalidType:
        assert True
