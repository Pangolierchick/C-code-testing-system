import subprocess as sb
import ts_text

PASSED = "\x1b[1;32;40mPASSED\033[0m"
FAILED = "\x1b[1;31;40mFAILED\033[0m"

class Test():
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



def unittest(exec_path:str, test_path:str):
    
    test_data = ts_text.parse_test_file(test_path)
    number_of_tests = len(test_data)

    test_list = []
    
    for i in range(len(test_data)):
        real_data = exec_file(exec_path, test_data[i]["input"])

        test_output = ts_text.get_numbers(test_data[i]["output"])
        test_exitcode = int(test_data[i]["exitcode"])

        test = Test(real_data["coll_data"], 
                    test_output, 
                    real_data["exitcode"] > 0, 
                    test_exitcode > 0, 
                    test_data[i]["title"])

        test_list.append(test)
    
    Tests = TestList(test_list)
    return Tests

def exec_file(path:str, data=None, ftype="int") -> dict:
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
        pr_vals["coll_data"] = ts_text.get_strings(pr.stdout)

    pr_vals["exitcode"] = pr.returncode

    return pr_vals

def compile(path, compiler="gcc-9", oname:str="main", keys:tuple=None, suppress=False):
    '''
    compiling file with given args
    return None
    '''

    if keys is None:
        keys = ["-Wall", "-Werror", "-Wextra", "-pedantic"]
    
    RESULT = PASSED
    
    
    keys.insert(0, path)
    keys.insert(0, compiler)
    
    if suppress:
        pass
        #keys.insert(2, " 2> /dev/null")
    
    keys.extend(["-o", oname.strip()])

    comp_data = sb.call(keys)
    
    if comp_data: 
        RESULT = FAILED
    
    return RESULT

