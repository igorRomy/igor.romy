"""
import sys
import subprocess

class t:

    procs = []
    for i in range(10):
        proc = subprocess.Popen([sys.executable, 'main.py', '{}in.csv'.format(i), '{}out.csv'.format(i)])
        procs.append(proc)

    for proc in procs:
        proc.wait()

"""