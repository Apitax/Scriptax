from scriptax.tests.pre_test import execute


def test_hex():
    scriptax = '''
    test = 0xabcdEF1234567890;
    return test;
    '''
    block_status, visitor = execute(scriptax)
    assert block_status.result == "0xABCDEF1234567890"