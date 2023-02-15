"""
obfuscator
Description: A basic python script to aid in the obfuscation of c and c++ source code files
Authors: Sam "Alice" Blair, Winston Howard, Chance Sweetser
Created Date: 05/04/20
Github: https://github.com/whoward3/C-Code-Obfuscator
"""

import os
import re
import random
import string


def rename_variables(given_string):
    """
    Function to rename all variables and fuctions.
    given_string is a string of C/C++ code
    """

    # Variable declarations:
    variable_dictionary = {}
    special_cases = {"typedef", "unsigned"}
    index = 0
    new_string = ""

    # Split the code to indicate when it enters/exits a string
    split_code = re.split('\"', given_string)

    # REGEX to find all function and variable declarations ignoring main
    filtered_code = re.findall(
        "(?:\w+\s+)(?!main)(?:\*)*([a-zA-Z_][a-zA-Z0-9_]*)", given_string)

    # For loop to add examples found from running a REGEX to a dictionary object
    # Ignores special cases and repeats
    # When a value is entered it is also assigned a random string of length 5
    for found_example in filtered_code:

        if (found_example not in special_cases):

            if (found_example not in variable_dictionary):

                variable_dictionary[found_example] = random_string(5)

    # For each even section in split code (odd indicates that it is in a string)
    # replace all of the varaible and function names with what is defined in the dictionary
    for section in split_code:

        if (index % 2 == 0):

            for entry in variable_dictionary:

                # Used \W because we dont want to replace a variable if it is inside another word.
                re_string = r"\W{}\W".format(entry)

                # While loop to go through every entry and replace it
                # Breaks when it cannot find another instance
                while True:
                    first_found_entry = re.search(re_string, section)
                    if (not first_found_entry):
                        break

                    # Gets the iterator start and enndpoints of the searched re_string
                    # Then replaces the the information inbetween with the dictionary value
                    start = first_found_entry.start(0)
                    end = first_found_entry.end(0)
                    section = section[:start+1] + \
                        variable_dictionary[entry] + section[end-1:]

        # Add the current section back to make the original string but with obfuscated names
        # Accounts for adding a quote everytime except for the first scenario
        if (index >= 1):
            new_string = new_string + "\"" + section
        else:
            new_string = new_string + section

        index += 1

    # Return the obfuscated code
    return new_string


def random_string(stringLength=8):
    return ''.join(random.choices(string.ascii_lowercase, k=5))


def main():
    """
    The main function to begin the obfuscation of c code files
    """
    cwd = os.getcwd()
    print("Looking for C Source Files in {}...".format(cwd))

    print("Log: ")
    for filename in os.listdir(cwd):
        # print("\n {} : \r".format(filename))
        if (".c" in filename or ".h" in filename):
            with open(os.path.join(cwd, filename)) as file_data:
                file_string = file_data.read()
                print("PASS\n")
                file_string = rename_variables(file_string)
                f = open("obfuscated_"+filename, "w+")
                f.write(file_string)
                print(file_string)

        else:
            print("FAIL")


if __name__ == "__main__":
    main()
