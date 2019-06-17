from scriptax.tests.pre_test import execute


def test_error():
    scriptax = '''
    test = "didn't work";
    error("worked");
    return test;
    '''
    block_status, visitor = execute(scriptax)
    assert block_status.result == None and visitor.is_error() and visitor.message == "worked"