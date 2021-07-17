"""
Bugs: Weird behavior when path is like `__pycache__/__pycache__`
    and using `dry_run` and `verbose` flags. NOT IMPORTANT.

Usage:
    $ python rm_pycache.py
    removed '__pycache__/line_count.pyc'
    removed '__pycache__/rm_pycache.pyc'
    removed directory '__pycache__'
"""
import sys
from pathlib import Path


def enclose(obj):
    """Get string representation of some object `obj` enclosed in quotes.
    """
    return repr(str(obj))


def remove_directory(path: Path, *, dry_run=False, verbose=True, verify=True):
    """Simulates `rm -r path` Unix command.
    Doesn't do anything if path doesn't exist or path is not a directory.

    dry_run: bool
        Runs the function without deleting any filesystem content.
    verbose: bool
        Logs what's being done.
    verify: bool
        Prompts before deleting each filesystem content.
    """
    if not path.is_dir():
        return

    if path.is_symlink():
        if not dry_run:
            path.unlink(missing_ok=True)
        if verbose:
            print(f"removed {enclose(path)}")
        return

    # Traverse directory content
    for f in path.glob('*'):
        if f.is_dir():
            remove_directory(
                f, dry_run=dry_run, verbose=verbose, verify=verify)
        elif f.is_file():
            if not dry_run:
                f.unlink(missing_ok=True)
            if verbose:
                print(f"removed {enclose(f)}")

    if not dry_run:
        path.rmdir()
    if verbose:
        print(f"removed directory {enclose(path)}")


def remove_pycache(
        base_path: Path, *, dry_run=False, verify=True, verbose=True):

    pycaches = filter(
        lambda f: f.is_dir(),
        base_path.rglob("__pycache__")
    )

    for f in pycaches:
        remove_directory(f, dry_run=dry_run, verbose=verbose, verify=verify)


if __name__ == "__main__":
    argc = len(sys.argv)
    argv = sys.argv

    path = "."

    if argc >= 2:
        path = argv[1]

    path = Path(path)
    remove_pycache(path)
