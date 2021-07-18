"""
Talia Discord Bot
GNU General Public License v3.0
console.py (Routine/Console)

Main console file
"""
import traceback
from Utils import other
from Routine.Console import control

_commands = {
    "control": control
}


def run(conn):
    """
    The main console input

    1. Gets message input
    2. Formats the message
    3. Runs the command if it exists
    """
    while True:
        msg = input()
        if len(msg) == 0:
            continue

        args, e_args = _parse_cmd(msg)
        args[0] = args[0].lower()

        if args[0] not in _commands:
            other.c_print(f"Unknown command: {args[0]}")
            continue

        try:
            _commands[args[0]].run(args, e_args, conn)
        except:
            exc_info = traceback.format_exc()
            other.log(f"Error occurred, traceback below\n{exc_info}", "critical")


def _parse_cmd(msg):
    """
    Formats message information

    1. Splits the message by spaces
    2. Checks for arguments that start with -
    3. Removes each argument that starts with - from
     the main arg list
    """
    args = []
    e_args = {}
    removed = []
    tmp = ""
    do_split = True

    for char in msg:
        if char == " " and do_split:
            args.append(tmp)
            tmp = ""
        elif char == "\"":
            do_split = not do_split
        else:
            tmp += char

    args.append(tmp)

    for arg in args:
        if not arg.startswith("-"):
            continue
        if len(arg) == 1:
            continue

        arg_split = arg.split(":", 1)
        removed.append(arg)

        if len(arg_split) == 1:
            e_args[arg_split[0]] = None
        else:
            e_args[arg_split[0]] = arg_split[1]

    for removed_arg in removed:
        args.remove(removed_arg)

    return args, e_args