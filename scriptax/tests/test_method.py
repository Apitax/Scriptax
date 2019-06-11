from scriptax.tests.pre_test import execute


def test_method():
    scriptax = '''
    script test()
    {
        return true;
    }
    return test();
    '''
    block_status, visitor = execute(scriptax)
    assert block_status.result == True


def test_method_2():
    scriptax = '''
    script test()
    {
        return true;
    }
    return self.test();
    '''
    block_status, visitor = execute(scriptax)
    assert block_status.result == True


def test_method_3():
    scriptax = '''
    static script test()
    {
        return true;
    }
    return self.test();
    '''
    block_status, visitor = execute(scriptax)
    assert block_status.result == True


def test_method_4():
    scriptax = '''
    static script test()
    {
        return true;
    }
    return test();
    '''
    block_status, visitor = execute(scriptax)
    assert block_status.result == True


def test_method_5():
    scriptax = '''
    script static test()
    {
        return true;
    }
    return test();
    '''
    block_status, visitor = execute(scriptax)
    assert block_status.result == True


def test_method_6():
    scriptax = '''
    static test()
    {
        return true;
    }
    return test();
    '''
    block_status, visitor = execute(scriptax)
    assert block_status.result == True


def test_method_7():
    scriptax = '''
    async test()
    {
        return true;
    }
    return test();
    '''
    block_status, visitor = execute(scriptax)
    assert block_status.result == True


def test_method_8():
    scriptax = '''
    script static async test()
    {
        return true;
    }
    return test();
    '''
    block_status, visitor = execute(scriptax)
    assert block_status.result == True


def test_method_9():
    scriptax = '''
    script other_test()
    {
        return "worked";
    }
    script static async test()
    {
        return other_test();
    }
    return test();
    '''
    block_status, visitor = execute(scriptax)
    assert block_status.result == "worked"


def test_method_10():
    scriptax = '''
    script other_test()
    {
        return "worked";
    }
    script static async test()
    {
        return self.other_test();
    }
    return self.test();
    '''
    block_status, visitor = execute(scriptax)
    assert block_status.result == "worked"


def test_method_11():
    scriptax = '''
    script other_test()
    {
        return "worked";
    }
    script static async test()
    {
        return other_test();
    }
    return self.test();
    '''
    block_status, visitor = execute(scriptax)
    assert block_status.result == "worked"


def test_method_12():
    scriptax = '''
    script other_test()
    {
        return "worked";
    }
    script static async test()
    {
        return self.other_test();
    }
    return test();
    '''
    block_status, visitor = execute(scriptax)
    assert block_status.result == "worked"


def test_method_13():
    scriptax = '''
    script other_test()
    {
        test = "worked";
    }
    script static async test_method()
    {
        self.other_test();
    }
    test = null;
    test_method();
    return test;
    '''
    block_status, visitor = execute(scriptax)
    assert block_status.result == "worked"


def test_method_14():
    scriptax = '''
    script other_test()
    {
        self.test = "worked";
    }
    script static async test_method()
    {
        other_test();
    }
    test = null;
    test_method();
    return test;
    '''
    block_status, visitor = execute(scriptax)
    assert block_status.result == "worked"


def test_method_15():
    scriptax = '''
    script other_test()
    {
        return "worked";
    }
    script static async test_method()
    {
        return other_test();
    }
    test = test_method;
    return test();
    '''
    block_status, visitor = execute(scriptax)
    assert block_status.result == "worked"


def test_method_16():
    scriptax = '''
    script static async test_method(my_return)
    {
        return my_return;
    }
    return test_method(my_return = "worked");
    '''
    block_status, visitor = execute(scriptax)
    assert block_status.result == "worked"


def test_method_17():
    scriptax = '''
    script other_test()
    {
        return "worked";
    }
    script static async test_method(my_callback)
    {
        return my_callback();
    }
    test = test_method;
    my_callback = other_test;
    return test(my_callback = my_callback);
    '''
    block_status, visitor = execute(scriptax)
    assert block_status.result == "worked"


def test_method_18():
    scriptax = '''
    script other_test()
    {
        return "worked";
    }
    script static async test_method(my_callback)
    {
        return my_callback();
    }
    return test_method(my_callback = other_test);
    '''
    block_status, visitor = execute(scriptax)
    assert block_status.result == "worked"


def test_method_19():
    scriptax = '''
    script other_test()
    {
        return "worked";
    }
    script static async test_method(my_callback)
    {
        return my_callback();
    }
    return self.test_method(my_callback = other_test);
    '''
    block_status, visitor = execute(scriptax)
    assert block_status.result == "worked"


def test_method_20():
    scriptax = '''
    script other_test()
    {
        return "worked";
    }
    script static async test_method(my_callback)
    {
        return my_callback();
    }
    return self.test_method(my_callback = self.other_test);
    '''
    block_status, visitor = execute(scriptax)
    assert block_status.result == "worked"


def test_method_21():
    scriptax = '''
    script static async test_method(my_callback = "worked")
    {
        return "worked";
    }
    return self.test_method();
    '''
    block_status, visitor = execute(scriptax)
    assert block_status.result == "worked"


def test_method_22():
    scriptax = '''
    script test_method(my_callback = "worked")
    {
        return my_callback;
    }
    return test_method();
    '''
    block_status, visitor = execute(scriptax)
    assert block_status.result == "worked"


def test_method_23():
    scriptax = '''
    my_method = script other_test() {
        return "worked";
    };
    return my_method();
    '''
    block_status, visitor = execute(scriptax)
    assert block_status.result == "worked"


def test_method_24():
    scriptax = '''
    script test(my_callback)
    {
        return my_callback();
    }
    my_method = script other_test() {
        return "worked";
    };
    return test(my_callback=my_method);
    '''
    block_status, visitor = execute(scriptax)
    assert block_status.result == "worked"


def test_method_25():
    scriptax = '''
    script static async test_method(my_callback = script other_test() {return "worked";})
    {
        return my_callback();
    }
    return test_method();
    '''
    block_status, visitor = execute(scriptax)
    assert block_status.result == "worked"


def test_method_26():
    scriptax = '''
    script static async test_method(my_callback = script other_test(temp = "worked") {return temp;})
    {
        return my_callback();
    }
    return test_method();
    '''
    block_status, visitor = execute(scriptax)
    assert block_status.result == "worked"


def test_method_27():
    scriptax = '''
    script static async test_method(my_callback = script other_test(temp = "worked") {return temp;})
    {
        return my_callback(temp="test");
    }
    return test_method();
    '''
    block_status, visitor = execute(scriptax)
    assert block_status.result == "test"