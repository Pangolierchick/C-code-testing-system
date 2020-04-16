import sys
import os
import argparse
import subprocess as sb
import ts_tests
import ts_text

PASSED = "\x1b[1;32;40mPASSED\033[0m"
FAILED = "\x1b[1;31;40mFAILED\033[0m"
ERROR = "\x1b[1;31;40mERROR\033[0m"

def printFailed(tests:list):
    for num, test in enumerate(tests):
        if not test:
            print(f"\tTEST #{num + 1}\t\t\t\t{FAILED}")

def beuatiful_print(test_data:dict):
    for test, result in test_data.items():
        if test == "BUILD":
            print(f"{test:>7}\t\t........\t\t{result:>7}")
        if test == "TESTS":
            print(f"{test:>7}\t\t........\t\t{result[0]:>7} ({sum(result[1])} : {result[2]})")
            if result[0] == FAILED:
                printFailed(result[1])


def init_tests(args):
    test_data = {"BUILD": FAILED}

    cpath = os.path.abspath(args.cpath)
    testfilepath = os.path.abspath(args.testpath)

    compiledpath, extens = cpath.split(".") # /.../main.c -> /.../main

    if not ts_text.isCfile(cpath):
        print(f"{ERROR}: path {cpath} doesnt mark on C-file")
        return None
 
    if not ts_text.isexist(testfilepath):
        print(f"{ERROR}: path {testfilepath} doesnt mark on test file")
        return None
    
    test_data["BUILD"] = ts_tests.compile(cpath, oname=compiledpath)
    
    if test_data["BUILD"] == PASSED:
        tests = ts_tests.unittest(compiledpath, testfilepath)
        test_data["TESTS"] = tests

    beuatiful_print(test_data)



def main():
    parser = argparse.ArgumentParser(description="Test system 0.3.0")
    subparser = parser.add_subparsers()

    test = subparser.add_parser("test", help="execute file and check if it corrects with tests.")
    test.add_argument("-pt", "--testpath", help="This is path to test txt file.", default="./tests.txt")
    test.add_argument("-pc", "--cpath", help="This is path to executable file.", default="./main.c")
    test.set_defaults(func=init_tests)

    args = parser.parse_args()
    args.func(args)

if __name__ == "__main__":
    main()