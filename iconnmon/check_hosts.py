"""
Module for checking if a host is responding
"""

import platform
import subprocess
from ipaddress import ip_address

from shell import shell


def _check_ip(value: str) -> bool:
    """
    Validates the str is a valid ip v4 address
    """
    try:
        ip = ip_address(value)  # noqa: F841
        return_value = True
    except ValueError:
        return_value = False
    return return_value


def ping_host(host: str, output: str = None) -> bool | list:
    """
    Method for pinging a host
    """
    result = _check_ip(host)
    if result:
        param = "-n" if platform.system().lower() == "windows" else "-c"

        command = ["ping", param, "1", host]
        if output is None:
            result = subprocess.call(command) == 0
        else:
            execute_result = shell(command)
            result = execute_result.output()

    return result
