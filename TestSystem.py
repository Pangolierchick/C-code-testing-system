import sys
import os
import argparse
import subprocess as sb

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

def compile(path, compiler="gcc-9", oname:str="main", keys:tuple=["-Wall", "-Werror", "-Wextra", "-pedantic"]):
    '''
    compiling file with given args
    return None
    '''
    
    RESULT = "PASSED"
    
    keys.insert(0, path)
    keys.insert(0, compiler)
    keys.extend(["-o", oname.strip()])
    
    cmp_data = sb.call(keys)
    
    if cmp_data:
        RESULT = "FAILED"
    
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

def test():
    test_data = dict()
    

    pass

def init_tests(args):
    d = compile("./main.c", oname="b")
    '''
    for line in proc.stdout:
        print(line.strip())
    '''

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