# Katy Huang 59698946
from pathlib import Path
import os
import shutil


def dir_input() -> list:
    """
    The function reads an input line that tells us which files are eligible to be found(D/R),
    followed by the path to a directory. If input is invalid, the function will keep asking
    until the input is valid. The function will return a list, where the first element of the
    list is a string that is either 'D' or 'R' and the second element of the list is the path to
    a directory.
    """
    Valid = False
    while not Valid:
        directories_lst = input().split(' ', 1)
        if ((directories_lst[0] == 'D' or directories_lst[0] == 'R') and Path(directories_lst[1]).exists() == True):
            Valid = True
        else:
            print('ERROR')
    return [directories_lst[0], Path(directories_lst[1])]


def get_path(the_path: Path, file_lst=None, sub_lst=None) -> list:
    """
    The function return a list of paths to every file that is under consideration in the correct order.
    """
    if file_lst is None:
        file_lst = []
    if sub_lst is None:
        sub_lst = []
    if the_path.is_file():
        file_lst.append(the_path)
    else:
        for element in the_path.iterdir():
            sub_lst.extend(get_path(element))
        Ssub = sorted(sub_lst, key=str)
        file_lst.append(Ssub)
    return file_lst


def print_path(file_lst, path_lst=None):
    """
    The function print and return paths to every file that is under consideration in the correct order.
    """
    if path_lst is None:
        path_lst = []
    for element in file_lst:
        if type(element) != list:
            print(element)
            path_lst.append(element)
        elif type(element) == list:
            path_lst.extend(print_path(element))
    return path_lst


def search_input() -> list:
    """
    The function read input that indicate the search characteristics.
    The function return a list of string. 
    """
    Valid = False
    while not Valid:
        search_lst = input().split(' ', 1)
        if len(search_lst) == 1 and search_lst[0] != 'A':
            print('ERROR')
        elif len(search_lst) > 2:
            print('ERROR')
        elif search_lst[0] not in 'ANET<>':
            print('ERROR')
        elif len(search_lst) == 2 and search_lst[1] == '':
            print('Error')
        else:
            Valid = True
    return search_lst


def searching(file_lst: list, search_lst: list) -> list:
    """
    The function perform the searching on the file_list according
    to the search_lst return by the search_input function.
    The function return a list of path of interest.
    """
    interest_lst = []
    if search_lst[0] == 'A':
        interest_lst = file_lst
    elif search_lst[0] == 'N':
        for file in file_lst:
            if search_lst[1] == str(file)[-len(search_lst[1]):]:
                interest_lst.append(file)
    elif search_lst[0] == 'E':
        for file in file_lst:
            if search_lst[1] == str(file)[-len(search_lst[1]):]:
                if '.' in search_lst[1]:
                    if len(search_lst[1]) == len(str(file).split('.')[-1]) + 1:
                        interest_lst.append(file)
                else:
                    if len(search_lst[1]) == len(str(file).split('.')[-1]):
                        interest_lst.append(file)
    elif search_lst[0] == 'T':
        the_file = None
        for file in file_lst:
            try:
                the_file = open(file, 'r')
                data = the_file.read()
                if search_lst[1] in data:
                    interest_lst.append(file)
            except:
                pass
            finally:
                if the_file != None:
                    the_file.close()
    elif search_lst[0] == '<':
        for file in file_lst:
            size = os.path.getsize(file)
            if size < int(search_lst[1]):
                interest_lst.append(file)
    elif search_lst[0] == '>':
        for file in file_lst:
            size = os.path.getsize(file)
            if size > int(search_lst[1]):
                interest_lst.append(file)
    return interest_lst


def print_lst(interest_lst) -> None:
    """
    The function prints the paths to every file in the
    interest_lst that is return from searching function
    """
    for file in interest_lst:
        print(file)


def action_input() -> str:
    """
    The function read input that indicate what action to take.
    The function will keep asking input until the input is valid.
    The function return a character that indicate what action to take.
    """
    Valid = False
    while not Valid:
        action = input()
        if action == 'F' or action == 'D' or action == 'T':
            Valid = True
        else:
            print('ERROR')
    return action


def action(interest_lst, action) -> None:
    """
    The function perform action according to the action character 
    return by the action_input function.
    """
    if action == 'F':
        the_file = None
        for file in interest_lst:
            try:
                the_file = open(file, 'r')
                print(the_file.readline().strip(), end='\n')
            except:
                print('NOT TEXT')
            finally:
                if the_file != None:
                    the_file.close()
    elif action == 'D':
        for file in interest_lst:
            dup_path = str(file) + '.dup'
            shutil.copyfile(file, Path(dup_path))

    elif action == 'T':
        for file in interest_lst:
            file.touch(exist_ok=True)


if __name__ == '__main__':
    lst = dir_input()
    lst_file = get_path(lst[1])
    lst_path = print_path(lst_file)
    lst_search = search_input()
    lst_interest = searching(lst_path, lst_search)
    if len(lst_interest) > 0:
        print_lst(lst_interest)
        action_chr = action_input()
        action(lst_interest, action_chr)
