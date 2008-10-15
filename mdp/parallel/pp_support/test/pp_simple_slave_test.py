"""
Script for starting pp-slaves on remote machines.

For each slave machine an ssh connection is kept open. Over this connection
pp_slave_script.py is started in a new process. The pid is stored and can be
used to kill the process.
"""

import signal
import os
import time

import mdp.parallel as parallel
import mdp.parallel.pp_support as pp_support

slave_id = "sherrington"
script_path = "/home/wilbert/develop/workspace/MDP/mdp/parallel/pp_support"
nice = -19
port = 30007
timeout = 20
secret = "rosebud"
n_workers = 1

python_executable = "/home/wilbert/bin/python"
sys_paths = ["/home/wilbert/develop/workspace/MDP"]

ssh_proc, remote_pid = pp_support.start_slave(address=slave_id, port=port, 
                                            ncpus=n_workers, 
                                            secret=secret, timeout=20, 
                                            nice=nice, 
                                            script_path=script_path, 
                                            source_paths=sys_paths,
                                            python_executable=python_executable)

print "waiting"
time.sleep(5)

print "killing now..."

# killing the ssh connection only will not kill the process!
ssh_proc.stdin.write("kill %d\n" % remote_pid)
ssh_proc.stdin.flush()
time.sleep(0.2)
os.kill(ssh_proc.pid, signal.SIGKILL)
print "all killed"

