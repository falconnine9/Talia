"""
Talia Discord Bot
GNU General Public License v3.0
config.py (Routine/Console)

config console command
"""
from Utils import other


def run(args, e_args, conn):
    if len(args) < 2:
        other.c_print("No operation given")
        return

    if len(args) < 3:
        other.c_print("No config attribute given")
        return

    args[1] = args[1].lower()

    if args[1] == "read":
        _config_read(args, e_args)
    elif args[1] == "edit":
        _config_edit(args, e_args)
    else:
        other.c_print(f"Invalid operation: {args[1]}")


def _config_read(args, e_args):
    config_info = other.load_config().cvt_dict()
    attributes = []

    for attribute in config_info:
        if attribute == "token" and "-safe" in e_args.keys():
            attributes.append("token: *********")
        else:
            attributes.append(f"{attribute}: {config_info[attribute]}")

    print("\n".join(attributes))


def _config_edit(args, e_args):
    other.c_print("Unfinished :)")