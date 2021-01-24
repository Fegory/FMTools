import os
import glob
import shutil


# application constants
C_CONSOLE_IO_SYMBOL = ">>> "
C_MAX_USER_INPUT_WORDS = 9  # e.g. "ls -a -ifends .c .h" is a list of 5 inputs. The max is this constant value
C_NULL_INPUT = "ignore!_!this!_!input"


# private static variables
__inputs = [C_NULL_INPUT] * C_MAX_USER_INPUT_WORDS


def applet_default_command():
    pass


def fm_help():
    print("\t'quit' to stop this application, 'help' to show this help page.")
    print("\tOther supported tools: ls, cprc, mvrc")


def unknown_command():
    print("Unknown Command")


def print_list_by_lines(lst):
    for i in range(len(lst)):
        print(lst[i])


def ls():
    print_list_by_lines(os.listdir())


# Copies files of a specified ending in the filename to the specified directory ("." by default).
def copy_recursively(move=False):
    ends = []
    found_ends = False
    for i in range(len(__inputs)):
        if __inputs[i] == "-ifends":
            found_ends = True
            break
    if not found_ends:
        print("No -ifends flag found")
        return
    for j in range(i+1, len(__inputs)):
        if len(__inputs[j]) == 0 or __inputs[j][0] == '-' or __inputs[j] == C_NULL_INPUT:
            break
        ends.append(__inputs[j])
        if __inputs[j] == "*":
            ends = ['']  # a list of length one, containing the empty string as it's only element
            break
    if len(ends) == 0:
        print("ERROR: No filename endings identified, three examples are .c .txt .py (the '.' needs to be explicit).\n"
              "Or, to affect all subfiles, use *, e.g.   cprc -ifends *    or   mvcprc -ifends *  .")
        return

    src = "."  # copies all files in src and in its child folders to dst
    for i in range(len(__inputs)):
        if __inputs[i] == "-src":
            if (i + 1) < len(__inputs):
                src = __inputs[i + 1]
            else:
                print("ERROR: Source directory should be specified after the -src flag.")
                return
            break

    dst = "."  # the copied files will be moved into this directory
    for i in range(len(__inputs)):
        if __inputs[i] == "-dst":
            if (i + 1) < len(__inputs):
                dst = __inputs[i + 1]
            else:
                print("ERROR: Destination directory should be specified after the -src flag.")
                return
            break
    files = []
    for e in ends:
        files += glob.glob(src + "/**/*" + e, recursive=True)
    for file in files:
        if not move:
            shutil.copy(file, dst)
        else:
            shutil.move(file, dst)


# moves files of a specified ending in the filename to the specified directory ("." by default).
def move_recursively():
    copy_recursively(move=True)


applet_switch = {  # dictionary, input is a one-word, lower-case string
    "": applet_default_command,
    "exit": quit,
    "quit": quit,
    "help": fm_help,
    "ls": ls,
    "cprc": copy_recursively,
    "mvrc": move_recursively,
}


def reset_inputs():
    for i in range(C_MAX_USER_INPUT_WORDS):
        __inputs[i] = C_NULL_INPUT


def main():
    print("\n    **** Running FMTools *****\n")
    while True:
        user_command = input(C_CONSOLE_IO_SYMBOL).strip()
        reset_inputs()
        if len(user_command) > 0:  # skip empty inputs
            ucs = user_command.split()  # list of input parameters (seperated by whitespace)
            for i in range(len(ucs)):
                __inputs[i] = ucs[i]
            __inputs[0] = ucs[0].lower()                        # first word is the applet mode
            applet_switch.get(__inputs[0], unknown_command)()   # run the chosen function


if __name__ == '__main__':
    main()
