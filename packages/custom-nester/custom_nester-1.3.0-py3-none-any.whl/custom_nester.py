"""This is the custom_nester.py module, it provides the function called
print_lol() which prints lists that may or may not include nested lists."""

import sys

def print_lol(the_list, indent = False, level=0, print_in = sys.stdout):
    """This function takes a positional argument called 'the_list', which is any python list
    (of, possibly nested lists). Each data item in the provided list is recursively printed
    to the screen on its own line.
    
    ---Arguments----------(default value)
    1st - 'the_list'
    2nd - 'indent' is used to activate the indentation. (False)
    3rd - 'level' is used to insert tab-stops when a nested list is encontered. (0)
    4th - 'print_in' gives us the ability to print the output in separated files or screen. (sys.stdout)
    ----------------------"""

    for each_item in the_list:
        if isinstance(each_item, list):
            print_lol(each_item, indent, level + 1, print_in)
        else:
            if indent:
                for tab_stop in range(level):
                    print("\t", end='', file = print_in)
            print(each_item, file = print_in)
