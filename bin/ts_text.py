import os

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

def isexist(path:str) -> bool:
    return os.path.isfile(path)


def isCfile(path:str) -> bool:
    """
    Checking if path marks on existing file
    and that file is C-file
    """
    if not isexist(path):
        return False
    
    name, ext = path.split(".")
    if ext == "c":
        return True
    return False