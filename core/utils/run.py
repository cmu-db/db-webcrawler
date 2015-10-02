from subprocess import PIPE, Popen
from multiprocessing import Pool

def get_process_children(pid):
    p = Popen('ps --no-headers -o pid --ppid %d' % pid, shell = True, stdout = PIPE, stderr = PIPE)
    stdout, stderr = p.communicate()
    return [int(p) for p in stdout.split()]

def run(args, cwd = None, shell = True, env = None):
    '''
    Run a command
    '''
    p = Popen(args, shell = shell, executable = '/bin/bash', cwd = cwd, stdout = PIPE, stderr=PIPE, env = env)
    stdout, stderr = '', ''
    stdout, stderr = p.communicate()
    return p.returncode, stdout, stderr

def run_command(command, timeout=1000):
    return run(command)

def run_command_async(command, timeout=1000):
    pool = Pool(processes=1)
    return pool.apply_async(run_command, [command, timeout]), pool