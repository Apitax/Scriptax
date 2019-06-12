from scriptax.tests.pre_test import execute


def test_comments():
    scriptax = '''
    /*
    I am a test
    */
    static async script other_test()
    {
        /*
        I am a test
        */
        return "worked";
        /*
        I am a test
        */
    }
    /*
    I am a test
    */
    script test()
    {
        /*
        I am a test
        */
        return true;
        /*
        I am a test
        */
    }
    /*
    I am a test
    */
    return test();
    /*
    I am a test
    */
    '''
    block_status, visitor = execute(scriptax)
    assert block_status.result == True


def test_comments_2():
    scriptax = '''
    // another type of test with some keywords like return if and for inside
    // if
    //continue
    /*
    I am a test
    */
    // another type of test with some keywords like return if and for inside
    // if
    //continue
    static async script other_test()
    {
        // another type of test with some keywords like return if and for inside
    // if
    //continue
        /*
        I am a test
        */
            // another type of test with some keywords like return if and for inside
    // if
    //continue
        // another type of test with some keywords like return if and for inside
    // if
    //continue
        return "worked";
        /*
        I am a test
        */
            // another type of test with some keywords like return if and for inside
    // if
    //continue
    }
        // another type of test with some keywords like return if and for inside
    // if
    //continue
    /*
    I am a test
    */
        // another type of test with some keywords like return if and for inside
    // if
    //continue
    script test()
    {
        // another type of test with some keywords like return if and for inside
    // if
    //continue
        /*
        I am a test
        */
            // another type of test with some keywords like return if and for inside
    // if
    //continue
        return true;
            // another type of test with some keywords like return if and for inside
    // if
    //continue
        /*
        I am a test
        */
            // another type of test with some keywords like return if and for inside
    // if
    //continue
    }
        // another type of test with some keywords like return if and for inside
    // if
    //continue
    /*
    I am a test
    */
        // another type of test with some keywords like return if and for inside
    // if
    //continue
    return test();
        // another type of test with some keywords like return if and for inside
    // if
    //continue
    /*
    I am a test
    */
        // another type of test with some keywords like return if and for inside
    // if
    //continue
    '''
    block_status, visitor = execute(scriptax)
    assert block_status.result == True