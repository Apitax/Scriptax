from scriptax.tests.pre_test import execute


def test_inheritance():
    scriptax = '''
    from scriptax import base;
    extend base;
    return left();
    '''
    block_status, visitor = execute(scriptax)
    assert block_status.result == "right"


def test_inheritance_2():
    scriptax = '''
    from scriptax import base;
    extend base;
    script up()
    {
        return "worked";
    }
    return up();
    '''
    block_status, visitor = execute(scriptax)
    assert block_status.result == "worked"


def test_inheritance_3():
    scriptax = '''
    from scriptax import base;
    extend base;
    script up()
    {
        return "worked";
    }
    return self.up();
    '''
    block_status, visitor = execute(scriptax)
    assert block_status.result == "worked"


def test_inheritance_4():
    scriptax = '''
    from scriptax import second_layer;
    extend second_layer;
    return up();
    '''
    block_status, visitor = execute(scriptax)
    assert block_status.result == "sky"


def test_inheritance_5():
    scriptax = '''
    from scriptax import second_layer;
    extend second_layer;
    return left();
    '''
    block_status, visitor = execute(scriptax)
    assert block_status.result == "right"


def test_inheritance_6():
    scriptax = '''
    from scriptax import base;
    extend base;
    return test;
    '''
    block_status, visitor = execute(scriptax)
    assert block_status.result == None


def test_inheritance_7():
    scriptax = '''
    from scriptax import second_layer;
    extend second_layer;
    return test;
    '''
    block_status, visitor = execute(scriptax)
    assert block_status.result == "worked"


def test_inheritance_8():
    scriptax = '''
    from scriptax import second_layer;
    extend second_layer;
    test = true;
    return test;
    '''
    block_status, visitor = execute(scriptax)
    assert block_status.result == True


def test_inheritance_9():
    scriptax = '''
    from scriptax import second_layer;
    extend second_layer;
    return big_test();
    '''
    block_status, visitor = execute(scriptax)
    assert block_status.result == "worked worked"


def test_inheritance_10():
    scriptax = '''
    from scriptax import second_layer;
    from scriptax import advanced_testing;
    extend second_layer with advanced_testing;
    return big_test();
    '''
    block_status, visitor = execute(scriptax)
    assert block_status.result == "worked worked"


def test_inheritance_11():
    scriptax = '''
    from scriptax import second_layer;
    from scriptax import advanced_testing;
    extend second_layer with advanced_testing;
    return day(param="day and");
    '''
    block_status, visitor = execute(scriptax)
    assert block_status.result == "day and night"
