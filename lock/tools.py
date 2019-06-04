from getpass import getpass
from os import chdir, getcwd
from pathlib import Path
from shutil import make_archive, rmtree


def get_password() -> str:
    while True:
        passw = getpass()
        conf_passw = getpass("Confirm Password: ")
        if passw != conf_passw:
            print("Passwords do not match.")
        else:
            break
    return passw


def ensure_file(file_location: Path):
    if file_location.is_dir():
        target_dir = str(file_location.absolute())
        past_cwd = getcwd()
        chdir(str(file_location.parent.absolute()))
        path = make_archive(target_dir, format="gztar", base_dir=file_location.stem)
        chdir(past_cwd)
        rmtree(file_location)
        return path
    elif file_location.is_file():
        return file_location.absolute()
    else:
        print("Unknown file / directory specified.")
        exit(1)
#
#
# def getch
#
# class _Getch:
#     """Gets a single character from standard input.  Does not echo to the screen."""
#     def __init__(self):
#         try:
#             self.impl = _GetchWindows()
#         except ImportError:
#             self.impl = _GetchUnix()
#
#     def __call__(self): return self.impl()
#
#
# class _GetchUnix:
#     def __init__(self):
#         import tty, sys
#
#     def __call__(self):
#         import sys
#         import tty
#         import termios
#         fd = sys.stdin.fileno()
#         old_settings = termios.tcgetattr(fd)
#         try:
#             tty.setraw(sys.stdin.fileno())
#             ch = sys.stdin.read(1)
#         finally:
#             termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
#         return ch
#
#
# class _GetchWindows:
#     def __init__(self):
#         import msvcrt
#
#     def __call__(self):
#         import msvcrt
#         return msvcrt.getch()
