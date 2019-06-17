from scriptax.tests.pre_test import execute


def test_switch_default():
    scriptax = '''
    test = "worked";
    test_result = false;
    switch {
        case(test == 5) {
            
        }
        case(test == "worked!")
        {
        
        }
        default {
            self.test_result = true;
        }
    
    }
    return test_result;
    '''
    block_status, visitor = execute(scriptax)
    assert block_status.result == True


def test_switch_case():
    scriptax = '''
    test = "worked";
    test_result = false;
    switch {
        case(test == 5) {

        }
        case(test == "worked")
        {
            self.test_result = "yes";
        }
        default {
            self.test_result = true;
        }

    }
    return test_result;
    '''
    block_status, visitor = execute(scriptax)
    assert block_status.result == "yes"


def test_switch_case_return():
    scriptax = '''
    test = "worked";
    test_result = false;
    switch {
        case(test == 5) {

        }
        case(test == "worked")
        {
            self.test_result = "yes";
            return "worked";
        }
        default {
            self.test_result = true;
        }

    }
    return test_result;
    '''
    block_status, visitor = execute(scriptax)
    assert block_status.result == "worked"


def test_switch_case_return_2():
    scriptax = '''
    test = "worked";
    test_result = false;
    switch {
        case(test == "worked") {

        }
        case(test == "worked")
        {
            self.test_result = "yes";
            return "worked";
        }
        default {
            self.test_result = true;
        }

    }
    return test_result;
    '''
    block_status, visitor = execute(scriptax)
    assert block_status.result == False


def test_switch_case_form():
    scriptax = '''
    test = "worked";
    test_result = false;
    switch {
        default {
            return true;
        }

    }
    return test_result;
    '''
    block_status, visitor = execute(scriptax)
    assert block_status.result == True


def test_switch_case_form_2():
    scriptax = '''
    test = "worked";
    test_result = false;
    switch {
        case(test == null)
        {
            return true;
        }

    }
    return test_result;
    '''
    block_status, visitor = execute(scriptax)
    assert block_status.result == False