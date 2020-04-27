import os
import sys
import subprocess as sb
import ts_text

PASSED = "\x1b[1;32;40mPASSED\033[0m"
FAILED = "\x1b[1;31;40mFAILED\033[0m"

class Test():
    '''
    Using this class as struct.
    '''
    real_values = None
    test_values = None
    real_exit_status = None
    test_exit_status = None
    test_title = None
    
    test_status = None

    def __init__(self, rvals, tvals, rexit_status, texit_status, ts_title):
        self.real_values = rvals
        self.test_values = tvals
        self.real_exit_status = rexit_status
        self.test_exit_status = texit_status
        self.title = ts_title

        self.test_status = not ((self.real_values != self.test_values) or 
                            (self.real_exit_status != self.test_exit_status))

class TestList():
    '''
    It contains list of Tests objects
    Class has method that returns result of tests
    '''
    tests_list = None
    test_status = None
    
    def __init__(self, testList):
        self.tests_list = testList
        self.test_status = self.totalResult()

        if self.test_status:
            self.test_status = PASSED
        else:
            self.test_status = FAILED
        

    def totalResult(self):
        res = True
        for test in self.tests_list:
            res &= test.test_status
        return res
    
    def getSuccessful(self):
        len_ = 0
        for test in self.tests_list:
            len_ += test.test_status
        
        return len_
    
    def getLen(self):
        return len(self.tests_list)


def style_test(spath:str, cpath:str):
    style = sb.call([spath, cpath])
    result = FAILED if style else PASSED
    return result
    

def unittest(exec_path:str, test_path:str, test_type:str="int", quite_ecode=None, key=None):
    print(test_type, quite_ecode, key)
    test_data = ts_text.parse_test_file(test_path)
    number_of_tests = len(test_data)

    test_list = []
    
    for i in range(len(test_data)):
        real_data = exec_file(exec_path, test_data[i]["input"], ftype=test_type, key=key)

        if test_type == "int":
            test_output = ts_text.get_numbers(test_data[i]["output"])
        elif test_type == "str":
            test_output = ts_text.get_strings_from_tests(test_data[i]["output"])

        test_exitcode = int(test_data[i]["exitcode"])

        if not quite_ecode:
            # If quite_ecode == True we dont mansion on specific exit value
            # We interested only in exit statue - it can be either passed or failed
            real_data["exitcode"] = real_data["exitcode"] > 0
            test_exitcode = test_exitcode > 0

        test = Test(real_data["coll_data"], 
                    test_output, 
                    real_data["exitcode"], 
                    test_exitcode, 
                    test_data[i]["title"])

        test_list.append(test)
    
    Tests = TestList(test_list)
    return Tests

def exec_file(path:str, data=None, ftype="int", key=None) -> dict:
    '''
    path to exec. file
    type: "int" or "str"
    data: string of given values to execution file
    return: typed val from stdout
    '''

    pr_vals = {"coll_data": None, "exitcode": 0}
    pr = sb.run([path], capture_output=True, encoding="utf-8", input=data)
    
    if ftype == "int":
        pr_vals["coll_data"] = ts_text.get_numbers(pr.stdout)

    elif ftype == "str":
        pr_vals["coll_data"] = ts_text.get_strings_from_exec(pr.stdout, key)

    pr_vals["exitcode"] = pr.returncode

    return pr_vals

def compile(wdir, flist, compiler="gcc-9", oname:str=None, keys:tuple=None, suppress=False, debug=False):
    '''
    compiling file with given args
    return PASSED or FAILED depending on build result
    '''

    if keys is None:
        keys = ["-Wall", "-Wextra", "-pedantic"]
    
    RESULT = PASSED
    
    
    for file in flist:
        keys.insert(0, os.path.join(wdir, file))

    keys.insert(0, compiler)
    
    if suppress:
        pass
        #keys.insert(2, " 2> /dev/null")
    keys.extend(["-o", oname])

    if debug:
        print(f"[debug] Starting build, keys: {keys}")

    comp_data = sb.call(keys)
    
    if comp_data: 
        RESULT = FAILED
    
    return RESULT

