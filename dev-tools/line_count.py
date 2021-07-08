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
import os

config = {}
if os.path.exists("lc_config.json"):
    with open("lc_config.json") as json_f:
        config = json.load(json_f)


def handle_dir(path):
    if not os.path.exists(path):
        return 0

    if not os.path.isdir(path):
        return 0

    if "ignored_folders" in config:
        path_split = path.split("/")
        if path_split[len(path_split) - 1] in config["ignored_folders"]:
            return 0

    local_count = 0

    for file in os.listdir(path):
        if os.path.isdir(f"{path}/{file}"):
            local_count += handle_dir(f"{path}/{file}")
        else:
            local_count += handle_file(f"{path}/{file}")

    return local_count


def handle_file(path):
    if not os.path.exists(path):
        return 0

    if os.path.isdir(path):
        return 0

    if "ignored_files" in config:
        path_split = path.split("/")
        if path_split[len(path_split) - 1] in config["ignored_files"]:
            return 0

    with open(path) as f:
        return len(f.readlines())


if __name__ == "__main__":
    print("Counting..")

    count = 0

    for folder in os.listdir():
        if os.path.isdir(folder):
            count += handle_dir(folder)
        else:
            count += handle_file(folder)

    print(f"{count} lines counted")