from scriptax.tests.pre_test import execute


def test_while():
    scriptax = '''
    i = 0;
    while(i < 10) {
        i++;
    }
    return i;
    '''
    block_status, visitor = execute(scriptax)
    assert block_status.result == 10


def test_while_2():
    scriptax = '''
    i = 0;
    j = 0;
    while(i < 10) {
        self.i++;
        if(self.i % 2 == 0)
            continue;
        self.j++;
    }
    return j;
    '''
    block_status, visitor = execute(scriptax)
    assert block_status.result == 5


def test_while_3():
    scriptax = '''
    i = 0;
    j = 0;
    while(i < 10) {
        self.i++;
        if(self.i % 2 == 0)
            continue;
        self.j++;
    }
    return j;
    '''
    block_status, visitor = execute(scriptax)
    assert block_status.result == 5


def test_while_4():
    scriptax = '''
    i = 0;
    while(i < 10) {
        if(i == 5)
            done;
        i++;
    }
    return i;
    '''
    block_status, visitor = execute(scriptax)
    assert block_status.result == 5


def test_while_5():
    scriptax = '''
    i = 0;
    while(i < 10) {
        if(i == 5)
            return 3;
        i++;
    }
    return i;
    '''
    block_status, visitor = execute(scriptax)
    assert block_status.result == 3