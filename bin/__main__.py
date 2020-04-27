import sys
import os
import argparse
import subprocess as sb
import ts_tests
import ts_text
from time import perf_counter

MY_VERSION = "0.6.0"
PASSED = "\x1b[1;32;40mPASSED\033[0m"
FAILED = "\x1b[1;31;40mFAILED\033[0m"
ERROR = "\x1b[1;31;40mERROR\033[0m"

def verbosePrint(tests:list, ver_code, print_all:bool=None):
    for num, test in enumerate(tests.tests_list):
        if print_all or not test.test_status: # Here we either printing all test or only failed tests
            rstatus = "FAILED" if test.real_exit_status else "SUCCESS"
            tstatus = "FAILED" if test.test_exit_status else "SUCCESS"
            
            if ver_code:
                rstatus = f"({test.real_exit_status} : {rstatus})"
                tstatus = f"({test.test_exit_status} : {tstatus})"

            print(f"\t\x1b[1;35;40mTEST {test.title}\033[0m\t\t\t\t{PASSED if test.test_status else FAILED}")
            print(f"Real values: {test.real_values}")
            print(f"Expected values: {test.test_values}")
            print(f"Real exit status: {rstatus}")
            print(f"Expected exit status: {tstatus}")


def result_print(test_data:dict, quite:bool, verbose_ec:bool=False, verbose_truetest:bool=None):
    build = test_data['BUILD']
    unittests = test_data['TESTS']
    print(f"BUILD\t\t........\t\t{build}")
    print(f"TESTS\t\t........\t\t{unittests.test_status} ({unittests.getSuccessful()} : {unittests.getLen()})")
    if (unittests.test_status == FAILED and not quite or verbose_truetest):
        verbosePrint(unittests, verbose_ec, print_all=verbose_truetest)


def init_tests(args):
    if args.version:
        print(f"The current version is {MY_VERSION}. Exiting.")
        sys.exit(0)

    if args.debug:
        print("[debug] given file list: ", *args.list)       
        start = perf_counter()
    test_data = {"BUILD": FAILED}

    work_dir = os.path.abspath(args.wdir)
    testfilepath = os.path.abspath(args.testpath)

    compiledpath = os.path.join(work_dir, "test_build")
    rootpath = os.path.split(os.path.dirname(sys.argv[0]))[0]

    '''

    Rework it for several files projects
    So i need to ask a question, do i really want to
    check files existence, because gcc can do it
    instead of me.


    if not ts_text.isCfile(cpath):
        print(f"{ERROR}: path {cpath} doesnt mark on C-file")
        return None
 
    if not ts_text.isexist(testfilepath):
        print(f"{ERROR}: path {testfilepath} doesnt mark on test file")
        return None
    '''

    test_data["BUILD"] = ts_tests.compile(work_dir, args.list, oname=compiledpath, debug=args.debug, compiler=args.compiler)

    if test_data["BUILD"] == PASSED:
        tests = ts_tests.unittest(compiledpath, testfilepath, quite_ecode=args.ecode_sensetive, test_type=args.type, key=args.key)
        test_data["TESTS"] = tests

    result_print(test_data, args.quite, args.ecode_sensetive, args.print_all)

    if args.style:
        for file in args.list:
            style = ts_tests.style_test(os.path.join(rootpath, "styleutil/CodeChecker"),
                                        os.path.join(work_dir, file))
            print(f"STYLE \t\t........\t\t{style} (for {file})")

    if args.debug:
        end = perf_counter()
        print(f"[debug] Elapsed time is {end - start:.3}s")
    


def main():
    parser = argparse.ArgumentParser(description=f"TestSystem {MY_VERSION}.\nMade by Kirill for my purposes and maybe someone else.", add_help=True, prog="Test system")
    subparser = parser.add_subparsers()

    test = subparser.add_parser("test", help="execute file and check if it corrects with tests.")
    test.add_argument("-t", "--testpath", help="This is path to test txt file.", default="./tests.txt", type=str)
    test.add_argument("-d", "--wdir", help="This is path to your project.", default="./", type=str)
    test.add_argument("--style", help="Check programm with bmstu style utility", action="store_true")
    test.add_argument("-q", "--quite", help="print less info, real data and test data and etc.", action="store_true")
    test.add_argument("--debug", help="Print debug info (you should use is only for debug puropuses)", action="store_true")
    test.add_argument("--type", help="What type of output tests you use: int, str. Default = int. \
                                      You also must input key for --key to parse test file correctly", default="int")
    test.add_argument("--key", help="Key for str type of tests. Default key: `Result:`", default="Result:", type=str)
    test.add_argument("--ecode_sensetive", help="Mansion not exit status, but specific exit code", action="store_true")
    test.add_argument("--print_all", help="Print all tests in final print. Without this key printing only failed tests", action='store_true')
    test.add_argument("-v", "--version", help="print version and exit", action="store_true")
    test.add_argument("--list", help="List of files to compile", nargs="+", default="main.c")
    test.add_argument("--compiler", help="what compiler should test system use", default="gcc")
    test.set_defaults(func=init_tests)

    args = parser.parse_args()
    try:
        args.func(args)
    except Exception as e:
        print(e)
        print(f"Type: -h or --help for help message")

if __name__ == "__main__":
    main()
