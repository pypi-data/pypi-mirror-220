import os
import platform
import subprocess

from e2e_cli.core.py_manager import PyVersionManager


def man_page():
    if platform.system() != "Windows":
        MAN_DIR = "/docs/e2e_cli.1"
        # print("curent folder(cli)", os.path.dirname(__file__))
        MAN_PATH = os.path.dirname(__file__)+MAN_DIR
        # print(MAN_PATH)
        subprocess.call(["man", MAN_PATH])
    else:
        print("Man page not available for windows")
