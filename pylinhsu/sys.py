import os
import sys
import importlib.util
from argparse import ArgumentParser, RawTextHelpFormatter
import getpass


def load_script(file_path):
    module_name = os.path.basename(file_path)[:-3]
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


def parse_arg_ang_get_config(prog="", description=""):
    parser = ArgumentParser(
        prog=prog, description=description, formatter_class=RawTextHelpFormatter
    )
    parser.add_argument("config_file_path", type=str, help="Config file path")
    args = parser.parse_args()
    config = load_script(args.config_file_path)
    return config


def get_password(msg=None):
    if not msg:
        msg = "Please input the password: "
    password = getpass.getpass(msg)
    return password
