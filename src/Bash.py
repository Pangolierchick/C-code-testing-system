from sys import argv
from os import path
from subprocess import call
from time import gmtime, strftime

def create_script(**kwargs):
    # ===== text =====
    if kwargs["d"]:
        main_dir = "-d " + kwargs["d"]
    else:
        main_dir = ""

    if kwargs["t"]:
        path_to_tests = "-t " + kwargs["t"]
    else:
        path_to_tests = ""

    if kwargs["type"]:
        type_of_test = "--type " + kwargs["type"]
    else:
        type_of_test = ""
    
    if kwargs["type"] == "str":
        key_for_str_tests = "--key " + kwargs["key"]
    else:
        key_for_str_tests = ""
    
    compiler = "--compiler " + kwargs["compiler"]

    # ===== bool =====
    check_for_exit_code = "--ecode_sensetive" if kwargs["ecode_sensetive"] else ""
    print_all_inf = "--print_all" if kwargs["print_all"] else ""
    is_style_check = "--style" if kwargs["style"] else ""
    quite = "--q" if kwargs["q"] else ""
    version = "--v" if kwargs["v"] else ""
    debug = "--debug" if kwargs["debug"] else ""

    # ===== list =====
    list_of_files = kwargs["list"]



    cur_dir, _ = path.split(argv[0])

    if path.exists(path.join(cur_dir, "main.py")):
        line = "python3 "
        line += path.join(cur_dir, "main.py")
    else:
        line = path.join(cur_dir, "TestSystem")

    line += " test "
    line += main_dir + " "
    line += path_to_tests + " "
    line += type_of_test + " "
    line += key_for_str_tests + " "
    line += compiler + " "
    
    line += check_for_exit_code + " "
    line += print_all_inf + " "
    line += is_style_check + " "
    line += quite + " "
    line += version + " "
    line += debug + " "

    line += "--list " + " ".join(list_of_files)

    script_path = "./init_tests"

    with open(script_path, "w") as script:
        script.write('#!/bin/bash\n')
        script.write("#This is auto-generated script. Do not modify it\n")
        script.write("#due to it will regenerate in next execution of main test script\n")
        script.write('#Made by pangolierchick.\n')
        script.write(f'#Timestamp: {strftime("%Y-%m-%d %H:%M:%S", gmtime())}\n')
        script.write(line)
    
    call(["chmod", "+x", script_path])

    return script_path
    
    
    
