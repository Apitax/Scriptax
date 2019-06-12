from scriptax.tests.pre_test import execute


def test_dict_signal():
    scriptax = '''
    script test(one, two, three)
    {
        return one + two + three;
    }
    mydict = {"one": "what ", "two": "is ", "three": "this."};
    return test(...mydict);
    '''
    block_status, visitor = execute(scriptax)
    assert block_status.result == "what is this."


def test_dict_signal_2():
    scriptax = '''
    script test(one, two, three, four)
    {
        return one + two + three + four;
    }
    mydict = {"two": "is ", "four": " Neat."};
    mydict2 = {"three": "this."};
    return test(...mydict2, one="huh what ", ...mydict);
    '''
    block_status, visitor = execute(scriptax)
    assert block_status.result == "huh what is this. Neat."
