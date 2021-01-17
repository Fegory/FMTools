import os
import glob
import shutil

# application constants
CONSOLE_IO_SYMBOL = ">>> "
MAX_USER_INPUT_WORDS = 9  # e.g. "ls -a -ifends .c .h" is a list of 5 inputs. The max is this constant value
NULL_INPUT = "ignore!_!this!_!input"

# application local variables
__inputs = [NULL_INPUT] * MAX_USER_INPUT_WORDS


def applet_default_command():
    pass


def unknown_command():
    print("unknown command")


def print_list_by_lines(lst):
    for i in range(len(lst)):
        print(lst[i])


def ls():
    print_list_by_lines(os.listdir())


# Copies files of a specified ending in the filename to the specified directory ("." by default).
def copy_reccursively():
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
        if len(__inputs[j]) == 0 or __inputs[j][0] == '-' or __inputs[j] == NULL_INPUT:
            break
        ends.append(__inputs[j])
    if len(ends) == 0:
        print("No filename endings identified, three examples are .c .txt or .py (the '.' needs to be explicit)")
        return

    src = "."  # copies all files in src and in it's child folders to dst
    found_dir = False
    for i in range(len(__inputs)):
        if __inputs[i] == "-src":
            found_dir = True
            break
    if found_dir:
        if (i+1) < len(__inputs):
            src = __inputs[i+1]
        else:
            print("Source directory should be specified after the -src flag.")

    dst = "."  # the copied files will be moved into this directory
    found_dir = False
    for i in range(len(__inputs)):
        if __inputs[i] == "-dst":
            found_dir = True
            break
    if found_dir:
        if (i + 1) < len(__inputs):
            dst = __inputs[i + 1]
        else:
            print("Destination directory should be specified after the -src flag.")
    files = []
    for e in ends:
        files += glob.glob(src + "/**/*" + e, recursive=True)
    for file in files:
        shutil.copy(file, dst)


# dictionary, input is a one-word, lower-case string
applet_switch = {
    "": applet_default_command,
    "exit": quit,
    "quit": quit,
    "ls": ls,
    "cprc": copy_reccursively,
}


def resetinputs():
    for i in range(MAX_USER_INPUT_WORDS):
        __inputs[i] = NULL_INPUT


def main():
    print("\n    **** Running FMTools *****\n")
    while True:
        user_command = input(CONSOLE_IO_SYMBOL).strip()
        resetinputs()
        if len(user_command) > 0:
            ucs = user_command.split()
            applet = ucs[0].lower()            # first word is the applet mode
            for i in range(len(ucs)):
                __inputs[i] = ucs[i]
        else:  # no input, skip onwards
            continue

        __inputs[0] = applet
        applet_switch.get(__inputs[0], unknown_command)()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()
