import sys
import os
import argparse
import subprocess as sb

PASSED = "\x1b[1;32;40mPASSED\033[0m"
FAILED = "\x1b[1;31;40mFAILED\033[0m"

def parse_test_block(text, pos):
    test_dict = {}
    key = None

    for line in range(pos + 1, len(text)):
        if text[line].find("#") != -1:
            if text[line].find("#test") != -1:
                if len(test_dict) != 3:
                    return None
                return test_dict
            
            key = text[line][1:].strip()
            continue

        if key is not None:
            test_dict[key] = test_dict.get(key, "") + text[line].strip() + " "
    
    if len(test_dict) != 3:
        return None
    
    return test_dict

def clear_text(file_list):
    line = 0
    while line < len(file_list):
        file_list[line] = file_list[line].strip()
        if not file_list[line]:
            file_list.pop(line)
        line += 1
    return file_list
        


def parse_test_file(path:str):
    tests_list = []

    testf = open(path, "r")
    file = testf.readlines()
    file = clear_text(file)
    testf.close()
    
    test_dict = dict()
    for line in range(len(file)):
        if "#test" in file[line]:
            parsed_block = parse_test_block(file, line)
            if parsed_block is not None:
                tests_list.append(parsed_block)
    
    return tests_list
    

def get_strings(string:str) -> list:
    pass

def get_numbers(string:str) -> list:
    """
    get string and finds from it number
    """
    
    num_list = []
    for word in string.split():
        if word.isdigit():
            num_list.append(int(word))

    return num_list

def compile(path, compiler="gcc-9", oname:str="main", keys:tuple=["-Wall", "-Werror", "-Wextra", "-pedantic"], suppress=False):
    '''
    compiling file with given args
    return None
    '''
    
    RESULT = PASSED
    
    
    keys.insert(0, path)
    keys.insert(0, compiler)
    
    if suppress:
        pass
        #keys.insert(2, " 2> /dev/null")
    
    keys.extend(["-o", oname.strip()])
    

    #print(keys)

    cmp_data = sb.call(keys)
    
    if cmp_data:
        RESULT = FAILED
    
    return RESULT



def exec_file(path:str, data=None, ftype="int") -> dict:
    '''
    path to exec. file
    type: "int" or "str"
    data: string of given values to execution file
    return: typed val from stdout
    '''

    pr_vals = {"coll_data": None, "exit_code": 0}
    pr = sb.run([path], capture_output=True, encoding="utf-8", input=data)
    
    if ftype == "int":
        pr_vals["coll_data"] = get_numbers(pr.stdout)
    elif ftype == "str":
        pr_vals["coll_data"] = get_strings(pr.stdout)

    pr_vals["exit_code"] = pr.returncode

    return pr_vals

def beuatiful_print(test_data:dict):
    for test, result in test_data.items():
        if test == "BUILD":
            print(f"{test:>7}   ........   {result:>7}")
        if test == "TESTS":
            print(f"{test:>7}   ........   {result[0]:>7} ({result[1]} : {result[2]})")

def unittest(exec_path:str, test_path:str):
    test_data = parse_test_file(test_path)
    number_of_tests = len(test_data)
    test_list = []
    for i in range(len(test_data)):
        real_data = exec_file(exec_path, test_data[i]["input"])
        
        # print(real_data["coll_data"], get_numbers(test_data[i]["output"]))
        # print(real_data["exit_code"], int(test_data[i]["exitcode"]))
        
        if (real_data["coll_data"] != get_numbers(test_data[i]["output"]) or
            real_data["exit_code"] != int(test_data[i]["exitcode"])):
            test_list.append(0)
        else:
            test_list.append(1)
    
    if (sum(test_list) == number_of_tests):
        return (PASSED, sum(test_list), number_of_tests)
    return (FAILED, sum(test_list), number_of_tests)

def init_tests(args):
    test_data = {}

    test_data["BUILD"] = compile(args.execpath, oname=args.execpath[:-2], suppress=True)
    
    if test_data["BUILD"] == FAILED:
        return

    tests = unittest(args.execpath[:-2], args.testpath)
    test_data["TESTS"] = tests
    beuatiful_print(test_data)



def main():
    parser = argparse.ArgumentParser(description="Test system 0.2.0")
    subparser = parser.add_subparsers()

    test = subparser.add_parser("test", help="execute file and check if it corrects with tests.")
    test.add_argument("-pt", "--testpath", help="This is path to test txt file.")
    test.add_argument("-pe", "--execpath", help="This is path to executable file.")
    test.set_defaults(func=init_tests)

    args = parser.parse_args()
    args.func(args)

if __name__ == "__main__":
    main()