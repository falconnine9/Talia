"""
Talia Discord Bot
GNU General Public License v3.0
control.py (Routine/Console)

control console command
"""
import os
from Utils import other


def run(args, e_args, conn):
    if len(args) < 2:
        other.c_print("No control variable given")
        return

    if len(args) < 3:
        other.c_print("No value given")
        return

    if args[1] not in os.environ:
        other.c_print("No control variable found")
        return

    args[2] = args[2].lower()

    if args[2] == "enable":
        os.environ[args[1]] = "1"
        other.c_print(f"Control variable \"{args[1]}\" enabled")
    elif args[2] == "disable":
        os.environ[args[1]] = "0"
        other.c_print(f"Control variable \"{args[1]}\" disabled")
    else:
        other.c_print(f"Invalid value: {args[2]}")