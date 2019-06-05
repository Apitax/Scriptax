from scriptax.tests.pre_test import execute


def test_string():
    scriptax = '''
    test = "what's my name !@#$%^&*()-=_+[]{}|;':,./<>?\'\\";
    return test;
    '''
    block_status, visitor = execute(scriptax)
    assert block_status.result == "what's my name !@#$%^&*()-=_+[]{}|;':,./<>?\'\\"