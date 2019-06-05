from scriptax.tests.pre_test import execute


def test_log():
    scriptax = '''
    log("test");
    return true;
    '''
    block_status, visitor = execute(scriptax)
    assert block_status.result == True