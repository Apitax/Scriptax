from scriptax.tests.pre_test import execute


def test_import():
    scriptax = '''
    from scriptax import testing;
    return true;
    '''
    block_status, visitor = execute(scriptax)
    assert block_status.result == True


def test_import_2():
    scriptax = '''
    from scriptax import testing;
    return testing.get_test_static();
    '''
    block_status, visitor = execute(scriptax)
    assert block_status.result == "worked"


def test_import_3():
    scriptax = '''
    from scriptax import testing as bananas;
    return bananas.get_test_static();
    '''
    block_status, visitor = execute(scriptax)
    assert block_status.result == "worked"


def test_import_4():
    scriptax = '''
    import testing;
    return testing.get_test_static();
    '''
    block_status, visitor = execute(scriptax)
    assert block_status.result == "worked"