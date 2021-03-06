import sys
import os
import argparse
import subprocess as sb
from time import perf_counter

import Tests
import Text
import Bash

MY_VERSION = "0.7.9"
PASSED = "\x1b[1;32;40mPASSED\033[0m"
SKIPPED = "\x1b[1;33;40mSKIPPED\033[0m"
FAILED = "\x1b[1;31;40mFAILED\033[0m"
ERROR  = "\x1b[1;31;40mERROR\033[0m"

def verbosePrint(tests:list, ver_code, print_all:bool=None):
    for num, test in enumerate(tests.tests_list):
        if print_all or not test.test_status: # Here we either printing all test or only failed tests
            rstatus = "FAILED" if test.real_exit_status else "SUCCESS"
            tstatus = "FAILED" if test.test_exit_status else "SUCCESS"

            if ver_code:
                rstatus = f"({test.real_exit_status} : {rstatus})"
                tstatus = f"({test.test_exit_status} : {tstatus})"

            print(f"\t\x1b[1;35;40mTEST {test.title:30}\033[0m\t\t\t\t{PASSED if test.test_status else FAILED:^10}")
            print(f"Real values: {test.real_values}")
            print(f"Expected values: {test.test_values}")
            print(f"Real exit status: {rstatus}")
            print(f"Expected exit status: {tstatus}")

def result_print(test_data:dict, quite:bool, verbose_ec:bool=False, verbose_truetest:bool=None):
    build = test_data['BUILD']
    print(f"BUILD\t\t........\t\t{build}")
    if build != FAILED:
        func_tests = test_data['TESTS']
        print(f"TESTS\t\t........\t\t{func_tests.test_status} ({func_tests.getSuccessful()} : {func_tests.getLen()})")
        if ((func_tests.test_status == FAILED and not quite) or verbose_truetest):
            verbosePrint(func_tests, verbose_ec, print_all=verbose_truetest)


def init_tests(args):
    if args.version:
        print(f"Current version is {MY_VERSION}. Exiting.")
        sys.exit(0)

    if args.debug:
        print("[DBG] given file list: ", *args.list)
        print("[DBG] path to execution: ", args.exec)
        start = perf_counter()
    test_data = {"BUILD": FAILED}

    work_dir = os.path.abspath(args.wdir)
    testfilepath = os.path.join(work_dir, args.testpath)

    compiledpath = os.path.join(work_dir, "test_build")
    rootpath = os.path.split(os.path.dirname(sys.argv[0]))[0]

    if args.exec is None:
        test_data["BUILD"] = Tests.compile(work_dir, args.list, oname=compiledpath, debug=args.debug, compiler=args.compiler)
    else:
        compiledpath = os.path.join(work_dir, args.exec)
        test_data["BUILD"] = SKIPPED

    if test_data["BUILD"] in (PASSED, SKIPPED):
        tests = Tests.run_tests(compiledpath,
                               testfilepath,
                               quite_ecode=args.ecode_sensetive,
                               test_type=args.type,
                               key=args.key,
                               dbg=args.debug
                              )

        test_data["TESTS"] = tests

    result_print(test_data, args.quite, args.ecode_sensetive, args.print_all)

    if args.style:
        for file in args.list:
            style = Tests.style_test(rootpath,
                                        os.path.join(work_dir, file),
                                        isdbg=args.debug)
            print(f"STYLE \t\t........\t\t{style} (for {file})")

    if args.debug:
        end = perf_counter()
        print(f"[DBG] Elapsed time is {end - start:.3}s")

    if args.create_script:
        print("Creating script")
        path = Bash.create_script(t=args.testpath,
                                d=args.wdir,
                                style=args.style,
                                q=args.quite,
                                debug=args.debug,
                                type=args.type,
                                key=args.key,
                                ecode_sensetive=args.ecode_sensetive,
                                print_all=args.print_all,
                                v=args.version,
                                list=args.list,
                                compiler=args.compiler)
        print(f"Script created ({path})")

    sys.exit(not tests.totalResult())



def main():
    parser = argparse.ArgumentParser(description=f"TestSystem {MY_VERSION}.\nMade by Kirill for my purposes and maybe someone else.", add_help=True, prog="Test system")
    subparser = parser.add_subparsers()


    test = subparser.add_parser("test", help="execute file and check if it corrects with tests.")
    test.add_argument("-t", "--testpath", help="This is path to test txt file.", default="./tests.txt", type=str)
    test.add_argument("-d", "--wdir", help="This is path to your project.", default="./", type=str)
    test.add_argument("--style", help="Check programm with bmstu style utility", action="store_true")
    test.add_argument("-q", "--quite", help="print less info, real data and test data and etc.", action="store_true")
    test.add_argument("--debug", help="Print debug info (you should use it only for debug purposes)", action="store_true")
    test.add_argument("--type", help="What type of output tests you use: int, str, float. Default = int. \
                                      You also must input key for --key to parse test file correctly", default="int")
    test.add_argument("--key", help="Key for str type of tests. Default key: `Result:`", default="Result:", type=str)
    test.add_argument("--ecode_sensetive", help="Checking certains exit code. \
                                                By default we check only exit status, for example FAILED and PASSED. \
                                                With this key we check 1 and 3 for example", action="store_true")
    test.add_argument("--print_all", help="Print all tests in final print. Without this key printing only failed tests", action='store_true')
    test.add_argument("-v", "--version", help="print version and exit", action="store_true")
    test.add_argument("--list", help="List of files to compile", nargs="+", default="main.c")
    test.add_argument("--compiler", help="what compiler should test system use", default="gcc")
    test.add_argument("--create_script", help="This flag turning on creation of bash script after programm's run.", action="store_true")
    test.add_argument("--exec", help="Path to the execution file", default=None)
    test.set_defaults(func=init_tests)

    args = parser.parse_args()
    args.func(args)

    # try:
    #     args.func(args)
    # except Exception as e:
    #     print(f"ERROR: {e}\nType: -h or --help for help message")

if __name__ == "__main__":
    main()
