import os


def path_check(path):
    for file in os.listdir(path):
        if file == "venv":
            continue

        elif file == "__pycache__":
            for file2 in os.listdir(f"{path}/__pycache__"):
                os.remove(f"{path}/__pycache__/{file2}")
            os.rmdir(f"{path}/__pycache__")

        elif os.path.isdir(f"{path}/{file}"):
            path_check(f"{path}/{file}")


path_check(os.getcwd())