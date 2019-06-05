from scriptax.tests.pre_test import execute

def test_float():
    scriptax = '''
    test = 5.59087765554444111;
    return test;
    '''
    block_status, visitor = execute(scriptax)
    assert block_status.result == 5.59087765554444111