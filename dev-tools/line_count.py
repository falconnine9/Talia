"""
This script will count all the lines of all the
files in a project

If you want to add certain configuration options,
create a file named "lc_config.json" and follow
the guide below on what you can add

lc_config
 - "ignored_folders": A list of folder names
 that will be ignored if they are found
 - "ignored_files": A list of file names
 that will be ignored if they are found
"""
import json
import sys
from pathlib import Path


def handle_directory(path: Path, config=None, verbose=True):
    if not path.is_dir():
        return 0

    if config is None:
        config = {}

    if path.name in config.get("ignored_folders", ()):
        return 0

    local_count = 0

    for f in path.glob("*"):
        if f.is_dir():
            local_count += handle_directory(f, config)
        elif f.is_file():
            local_count += handle_file(f, config)

    if verbose:
        print(f"{local_count}\t\t{path}")

    return local_count


def handle_file(path: Path, config=None, verbose=True):
    if not path.is_file():
        return 0

    if config is None:
        config = {}

    if path.name in config.get("ignored_files", ()):
        return 0

    with open(path) as f:
        count = sum(1 for _ in f)

    if verbose:
        print(f"{count}\t\t{path}")

    return count


if __name__ == "__main__":
    argc = len(sys.argv)
    argv = sys.argv

    path = "."
    lc_config = "lc_config.json"

    if argc >= 2:
        path = argv[1]
    if argc >= 3:
        lc_config = argv[2]

    path = Path(path)
    lc_config = Path(lc_config)

    if lc_config.is_file():
        config = json.loads(lc_config.read_text())
    else:
        config = None

    count = 0

    if path.is_file():
        count += handle_file(path, config)
    elif path.is_dir():
        count += handle_directory(path, config)
