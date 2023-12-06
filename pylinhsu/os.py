import os
import socket
import subprocess
from pylinhsu import log


def get_hostname():
    return socket.gethostname()


def get_command_output(command, working_dir=".", environ={}):
    for k, v in environ.items():
        os.environ[k] = v
    cwd = os.getcwd()
    os.chdir(working_dir)
    log.info(f"Command: {command}")
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    os.chdir(cwd)
    return stdout.decode("utf-8")


def run_command(command, working_dir=".", environ={}):
    for k, v in environ.items():
        os.environ[k] = v
    cwd = os.getcwd()
    os.chdir(working_dir)
    log.info(f"Command: {command}")
    # os.system(command)
    subprocess.run(command)
    os.chdir(cwd)


def run_commands(commands, working_dir=".", environ={}):
    for k, v in environ.items():
        os.environ[k] = v
    cwd = os.getcwd()
    os.chdir(working_dir)
    for command in commands:
        log.info(f"Command: {command}")
        # os.system(command)
        subprocess.run(command)
    os.chdir(cwd)
