from scriptax.tests.pre_test import execute


def test_nesting():
    scriptax = '''
    test = true;
    taco = null;
    data = [];
    if(test)
    {
        taco = "tuesday";
        test = false;
        if(taco == "tuesday")
        {
            taco = "thursday";
            test = true;
            if(test)
            {
                test = "worked";
                data[] = test;
                data[] = taco;
            }
            data[] = test;
            data[] = taco;
        }
        data[] = test;
        data[] = taco;
    }
    data[] = test;
    data[] = taco;
    return data;
    '''
    block_status, visitor = execute(scriptax)
    assert block_status.result == ["worked", "thursday", "worked", "thursday", "worked", "thursday", "worked", "thursday"]


def test_nesting_2():
    scriptax = '''
    test = true;
    taco = null;
    data = [];
    if(test)
    {
        taco = "tuesday";
        test = false;
        if(taco == "tuesday")
        {
            taco = "thursday";
            test = true;
            if(test)
            {
                self.test = "worked";
                data[] = test;
                data[] = taco;
            }
            data[] = test;
            data[] = taco;
        }
        data[] = test;
        data[] = taco;
    }
    data[] = test;
    data[] = taco;
    return data;
    '''
    block_status, visitor = execute(scriptax)
    assert block_status.result == ["worked", "thursday", "worked", "thursday", "worked", "thursday", "worked", "thursday"]