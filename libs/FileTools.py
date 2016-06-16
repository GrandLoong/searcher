import sys
import os
import subprocess


def start(filepath):
    """
    Uses to the default OS software defined tool to 'open/start' a path

    Args:
        filepath (basestring): path to open

    """
    cmd = "start "
    if sys.platform == "darwin":
        cmd = "open "
    elif sys.platform == "linux2":
        cmd = "xdg-open "
    else:
        filepath = filepath.replace('/', '\\')
        if os.path.isfile(filepath):
            os.startfile(filepath)
            return
    command = '{0} "{1}"'.format(cmd, filepath)
    print "running command %s", command
    subprocess.Popen(command, shell=True)
