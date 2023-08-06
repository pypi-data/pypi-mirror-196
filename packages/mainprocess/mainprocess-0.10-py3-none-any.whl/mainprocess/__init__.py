import subprocess
import os


def mainprocess(cmd):
    if isinstance(cmd, str):
        cmd = [cmd]
    exefile = cmd[0]
    exefile = exefile.strip().strip('"').strip()
    exefile = os.path.normpath(exefile)
    exefile = f'"{exefile}"'
    try:
        arguments = cmd[1:]
    except Exception:
        arguments = []

    args_command = " ".join(arguments).strip()
    wholecommand = f'start "" {exefile} {args_command}'
    p = subprocess.Popen(wholecommand, shell=True)
    return p


