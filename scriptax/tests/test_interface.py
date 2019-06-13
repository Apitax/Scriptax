from scriptax.tests.pre_test import execute


def test_interface():
    scriptax = '''
    from scriptax import testing;
    extend with testing;
    return get_test_static();
    '''
    block_status, visitor = execute(scriptax)
    assert block_status.result == "worked"


def test_interface_2():
    scriptax = '''
    from scriptax import testing;
    from scriptax import advanced_testing;
    extend with testing, advanced_testing;
    return day();
    '''
    block_status, visitor = execute(scriptax)
    assert block_status.result == "good night"


def test_interface_3():
    scriptax = '''
    from scriptax import testing;
    from scriptax import advanced_testing;
    extend with testing, advanced_testing;
    return day(param="day and");
    '''
    block_status, visitor = execute(scriptax)
    assert block_status.result == "day and night"