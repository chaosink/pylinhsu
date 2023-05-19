import os
import subprocess
from pylinhsu import log


def get_process_output(process):
    process = subprocess.Popen(
        process, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    return stdout.decode('utf8')


def run_command(command, working_dir='.', environ={}):
    for k, v in environ.items():
        os.environ[k] = v
    cwd = os.getcwd()
    os.chdir(working_dir)
    log.info(f'Command: {command}')
    # os.system(command)
    subprocess.run(command)
    os.chdir(cwd)


def run_commands(commands, working_dir='.', environ={}):
    for k, v in environ.items():
        os.environ[k] = v
    cwd = os.getcwd()
    os.chdir(working_dir)
    for command in commands:
        log.info(f'Command: {command}')
        # os.system(command)
        subprocess.run(command)
    os.chdir(cwd)
