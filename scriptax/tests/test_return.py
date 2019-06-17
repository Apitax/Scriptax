from scriptax.tests.pre_test import execute


def test_return():
    scriptax = '''
    return "test";
    '''
    block_status, visitor = execute(scriptax)
    assert block_status.result == "test"


def test_return_2():
    scriptax = '''
    test = "worked";
    return self.test;
    '''
    block_status, visitor = execute(scriptax)
    assert block_status.result == "worked"
