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
    

    print(keys)

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
            print(f"{test:>7}   ........   {result:>7}")

def test():
    test_data = dict()


    pass

def init_tests(args):
    test_data = {}

    test_data["BUILD"] = compile(args.execpath, oname=args.execpath[:-2], suppress=True)
    
    if test_data["BUILD"] == FAILED:
        return

    a = exec_file(args.execpath[:-2], "2 2")
    test_data["TESTS"] = PASSED
    print(a)
    beuatiful_print(test_data)



def main():
    parser = argparse.ArgumentParser(description="Test system 0.1.0")
    subparser = parser.add_subparsers()

    test = subparser.add_parser("test", help="execute file and check if it corrects with tests.")
    test.add_argument("-pt", "--testpath", help="This is path to test txt file.")
    test.add_argument("-pe", "--execpath", help="This is path to executable file.")
    test.set_defaults(func=init_tests)

    args = parser.parse_args()
    args.func(args)

if __name__ == "__main__":
    main()