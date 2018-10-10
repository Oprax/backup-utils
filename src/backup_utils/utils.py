"""
Usefull function needed by the module.
"""

import os
import socket

from datetime import date


def which(program):
    """
    Fetch for the absolute path of a binary, same as `which` Unix command.

    :param program: Name of the program
    :type program: str
    :return: Absolute path of the program, or None if path not found.
    :rtype: str

    :Example:

    >>> which("ls")
    /bin/ls
    """
    def is_exe(fpath):
        return os.path.isfile(fpath) and os.access(fpath, os.X_OK)

    fpath, _ = os.path.split(program)
    if fpath:
        if is_exe(program):
            return program
    else:
        for path in os.environ["PATH"].split(os.pathsep):
            exe_file = os.path.join(path, program)
            if is_exe(exe_file):
                return exe_file

    return None


def hostname():
    """
    Return the hostname of the current machine.

    :return: the hostname of the current machine
    :rtype: str
    """
    if socket.gethostname().find(".") >= 0:
        return socket.gethostname()
    else:
        return socket.gethostbyaddr(socket.gethostname())[0]


def render(template):
    """
    Format the template using hostname variable and date of the day.

    :param template: string to format
    :param template: string to format

    :return: the rendered template
    :rtype: str

    :Example:
    
    >>> render("machine-{hostname}-{date}")
    """
    return template.format(hostname=hostname(), date=date.today())
