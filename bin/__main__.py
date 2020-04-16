import sys
import os
import argparse
import subprocess as sb
import ts_tests
import ts_text
from time import perf_counter

MY_VERSION = "0.5.0"
PASSED = "\x1b[1;32;40mPASSED\033[0m"
FAILED = "\x1b[1;31;40mFAILED\033[0m"
ERROR = "\x1b[1;31;40mERROR\033[0m"

def verbosePrint(tests:list):
    for num, test in enumerate(tests.tests_list):
        if not test.test_status:
            rstatus = "SUCCESS" if test.real_exit_status else "FAILED"
            tstatus = "SUCCESS" if test.test_exit_status else "FAILED"
            print(f"\t\x1b[1;35;40mTEST {test.title}\033[0m\t\t\t\t{FAILED}")
            print(f"Real values: {test.real_values}")
            print(f"Expected values: {test.test_values}")
            print(f"Real exit status: {rstatus}")
            print(f"Expected exit status: {tstatus}")


def result_print(test_data:dict, quite:bool):
    build = test_data['BUILD']
    unittests = test_data['TESTS']
    print(f"BUILD\t\t........\t\t{build}")
    print(f"TESTS\t\t........\t\t{unittests.test_status} ({unittests.getSuccessful()} : {unittests.getLen()})")
    if (unittests.test_status == FAILED and not quite):
        verbosePrint(unittests)


def init_tests(args):
    if args.debug:
        start = perf_counter()
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

    result_print(test_data, args.quite)

    if args.style:
        # print("\t\tSTARTING STYLE TEST")
        style = ts_tests.style_test(os.path.abspath("../styleutil/CodeChecker"), cpath)
        print(f"STYLE\t\t........\t\t{style}")


    if args.debug:
        end = perf_counter()
        print(f"Elapsed time is {end - start:.3}s")
    




def main():
    parser = argparse.ArgumentParser(description=f"TestSystem {MY_VERSION}", add_help=True, prog="Test system")
    subparser = parser.add_subparsers()

    test = subparser.add_parser("test", help="execute file and check if it corrects with tests.")
    test.add_argument("-pt", "--testpath", help="This is path to test txt file.", default="./tests.txt", type=str)
    test.add_argument("-pc", "--cpath", help="This is path to executable file.", default="./main.c", type=str)
    test.add_argument("--style", help="Check programm with bmstu style utility", action="store_true")
    test.add_argument("-q", "--quite", help="print less info, real data and test data and etc.", action="store_true")
    test.add_argument("--debug", help="Print debug info (you should use is only for debug puropuses)", action="store_true")
    test.set_defaults(func=init_tests)

    args = parser.parse_args()
    try:
        args.func(args)
    except Exception as e:
        print(f"Error {e} type: -h for help message")

if __name__ == "__main__":
    main()
