from scriptax.tests.pre_test import execute


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