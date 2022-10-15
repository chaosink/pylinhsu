import subprocess

def get_process_output(process):
    process = subprocess.Popen(process, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    return stdout.decode('utf8')
