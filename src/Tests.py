import os
import sys
import subprocess as sb

import Text


PASSED = "\x1b[1;32;40mPASSED\033[0m"
FAILED = "\x1b[1;31;40mFAILED\033[0m"

class Test():
    '''
    Using this class as struct.
    '''
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





def style_test(root:str, cpath:str, isdbg:bool=False):
    """
    Init bmstu test
    return colored result such as FAILED or PASSED
    """
    workdir = os.path.join(root, "styleutil/")

    if isdbg:
        print("[DBG] starting style checking")
        print("[DBG] total call is: ", workdir + "CodeChecker",
        "--rules " + os.path.abspath(workdir + "Rules.txt"), 
        os.path.abspath(cpath))


    style = sb.call([workdir + "CodeChecker", "--rules", workdir + "Rules.txt", cpath])
    result = FAILED if style else PASSED
    return result

def get_data_from_string(string, data_type, key=None):
    """
    Getting data from string, type can be either int or float or str.
    Key is basically start of necessary string. 
    Key is need only when we parse strings from executrion file
    output
    """
    data = []

    if data_type in ("int", "float"):
        data = Text.get_numbers(string, type_=data_type)

    elif data_type == "str":
        if key is None:
            data = Text.get_strings_from_tests(string)
        else:
            data = Text.get_strings_from_exec(string, key)

    return data
    

def unittest(exec_path:str, test_path:str, test_type:str="int", quite_ecode=None, key=None, args=None, dbg=False):
    """
    test_type - can be int, str, float depending 
    on what type of data we use

    quite_code - if true we check only exit status
    if false we checking specific exit code
    such as we write in test file #exitcode 1
    programm returned 2, so result of test - FAILED

    key - this attribute is optional and you should use it 
    only if you parsing strings from programm's output. 
    Basycally this is string's begin

    Testing file. First of all, parsing givet test file, 
    then we executing file with all tests,
    creating class object where we can find results
    and then returning it
    """
    test_data = Text.parse_test_file(test_path)
    number_of_tests = len(test_data)

    test_list = []
    
    for i in range(len(test_data)):
        real_data = exec_file(exec_path, data=test_data[i]["input"], ftype=test_type, key=key, args=args, dbg=dbg)

        test_output = get_data_from_string(test_data[i]["output"], test_type)

        test_exitcode = int(test_data[i]["exitcode"])

        if not quite_ecode:
            # If quite_ecode == True we dont mansion on specific exit value
            # We interested only in exit statue - it can be either passed or failed
            real_data["exitcode"] = abs(real_data["exitcode"]) > 0
            test_exitcode = abs(test_exitcode) > 0

        test = Test(real_data["coll_data"], 
                    test_output, 
                    real_data["exitcode"], 
                    test_exitcode, 
                    test_data[i]["title"])

        test_list.append(test)
    
    Tests = TestList(test_list)
    return Tests

def exec_file(path:str, data=None, ftype="int", key=None, args=None, dbg=False) -> dict:
    '''
    Executing file with given args, and reading programm's 
    output, collecting it and then returning
    '''

    if dbg:
        print("------EXECUTING FILE------")
        print(f"[DBG] PATH: {path}")
        print(f"[DBG] ARGS: {args}")
        print(f"[DBG] DATA: {data}")

    pr_vals = {"coll_data": None, "exitcode": 0}
    pr = sb.run([path, args], capture_output=True, encoding="utf-8", input=data)

    if dbg:
        print("[DBG] STDOUT:\n", pr.stdout)

    pr_vals["coll_data"] = get_data_from_string(pr.stdout, ftype, key)

    pr_vals["exitcode"] = pr.returncode

    if dbg:
        print(f"[DBG] collected data from file: {pr_vals}")
        print("--------------------------")

    return pr_vals


def compile(wdir, flist, compiler="gcc-9", oname:str=None, keys:tuple=None, suppress=False, debug=False):
    '''
    compiling file with given args
    return PASSED or FAILED depending on build result
    '''

    if keys is None:
        keys = ["-Wall", "-Wextra", "-pedantic", "-Werror"]
    
    RESULT = PASSED
    
    for file in flist:
        keys.insert(0, os.path.join(wdir, file))

    keys.insert(0, compiler)
    
    if suppress:
        pass
        # keys.insert(2, " 2> /dev/null")
    keys.extend(["-o", oname])

    if debug:
        print(f"[debug] Starting build, keys: {keys}")

    comp_data = sb.call(keys)
    
    if comp_data: 
        RESULT = FAILED
    
    return RESULT

