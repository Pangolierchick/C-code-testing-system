import subprocess as sb
import ts_text

PASSED = "\x1b[1;32;40mPASSED\033[0m"
FAILED = "\x1b[1;31;40mFAILED\033[0m"

def unittest(exec_path:str, test_path:str):
    
    test_data = ts_text.parse_test_file(test_path)
    number_of_tests = len(test_data)

    test_list = []
    
    for i in range(len(test_data)):
        real_data = exec_file(exec_path, test_data[i]["input"])
        
        # print(real_data["coll_data"], get_numbers(test_data[i]["output"]))
        # print(real_data["exit_code"], int(test_data[i]["exitcode"]))
        
        if (real_data["coll_data"] != ts_text.get_numbers(test_data[i]["output"]) or
            real_data["exitcode"] != int(test_data[i]["exitcode"])):
            test_list.append(0)
        else:
            test_list.append(1)
    
    if (sum(test_list) == number_of_tests):
        return (PASSED, test_list, number_of_tests)
    
    return (FAILED, test_list, number_of_tests)

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

