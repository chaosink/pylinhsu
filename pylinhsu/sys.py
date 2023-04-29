import os
import sys
import subprocess
import importlib.util
from pylinhsu import log


def get_process_output(process):
    process = subprocess.Popen(
        process, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    return stdout.decode('utf8')


def load_script(file_path):
    module_name = os.path.basename(file_path)[:-3]
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


def run_command(command, working_dir='.', environ={}):
    for k, v in environ.items():
        os.environ[k] = v
    cwd = os.getcwd()
    os.chdir(working_dir)
    log.info(f'Command: {command}')
    os.system(command)
    os.chdir(cwd)
