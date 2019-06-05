from scriptax.tests.pre_test import execute


def test_d_plus():
    scriptax = '''
    test = 5;
    test++;
    return test;
    '''
    block_status, visitor = execute(scriptax)
    assert block_status.result == 6


def test_d_plus_2():
    scriptax = '''
    test = 5.78;
    test++;
    return test;
    '''
    block_status, visitor = execute(scriptax)
    assert block_status.result == 6.78


def test_d_minus():
    scriptax = '''
    test = 5;
    test--;
    return test;
    '''
    block_status, visitor = execute(scriptax)
    assert block_status.result == 4


def test_d_minus_2():
    scriptax = '''
    test = 5.12;
    test--;
    return test;
    '''
    block_status, visitor = execute(scriptax)
    assert block_status.result == 4.12


def test_pe():
    scriptax = '''
    test = 5;
    test += 4;
    return test;
    '''
    block_status, visitor = execute(scriptax)
    assert block_status.result == 9


def test_pe_2():
    scriptax = '''
    test = 5;
    test += 4.55;
    return test;
    '''
    block_status, visitor = execute(scriptax)
    assert block_status.result == (5 + 4.55)


def test_pe_3():
    scriptax = '''
    test = 5;
    test += -4.8;
    return test;
    '''
    block_status, visitor = execute(scriptax)
    assert block_status.result == (5 - 4.8)


def test_me():
    scriptax = '''
    test = 5;
    test -= 4;
    return test;
    '''
    block_status, visitor = execute(scriptax)
    assert block_status.result == 1


def test_me_2():
    scriptax = '''
    test = 5;
    test -= 4.6;
    return test;
    '''
    block_status, visitor = execute(scriptax)
    assert block_status.result == (5 - 4.6)


def test_mue():
    scriptax = '''
    test = 5;
    test *= 4;
    return test;
    '''
    block_status, visitor = execute(scriptax)
    assert block_status.result == 20


def test_mue_2():
    scriptax = '''
    test = 5.34;
    test *= 0.54;
    return test;
    '''
    block_status, visitor = execute(scriptax)
    assert block_status.result == 2.8836


def test_de():
    scriptax = '''
    test = 12;
    test /= 4;
    return test;
    '''
    block_status, visitor = execute(scriptax)
    assert block_status.result == 3


def test_de_2():
    scriptax = '''
    test = 5.34;
    test /= 0.54;
    return test;
    '''
    block_status, visitor = execute(scriptax)
    assert block_status.result == (5.34 / 0.54)


def test_list_append():
    scriptax = '''
    test = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10];
    test[] = 11;
    return test;
    '''
    block_status, visitor = execute(scriptax)
    assert block_status.result == [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]


def test_list_append_2():
    scriptax = '''
    test = [];
    test[] = 0;
    return test;
    '''
    block_status, visitor = execute(scriptax)
    assert block_status.result == [0]


def test_list_append_3():
    scriptax = '''
    test = [];
    test[] = 0;
    test[] = 1;
    return test;
    '''
    block_status, visitor = execute(scriptax)
    assert block_status.result == [0, 1]