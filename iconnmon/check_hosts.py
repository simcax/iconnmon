"""
Module for checking if a host is responding
"""

import platform
import subprocess
from ipaddress import ip_address

from shell import shell


class IConnMonPing:
    """
    Utiliy class with ping functionality
    """

    def _check_ip(self, value: str) -> bool:
        """
        Validates the str is a valid ip v4 address
        """
        try:
            ip = ip_address(value)  # noqa: F841
            return_value = True
        except ValueError:
            return_value = False
        return return_value

    def ping_host(self, host: str, output: str = None) -> bool | list:
        """
        Method for pinging a host
        """
        result = self._check_ip(host)
        if result:
            param = "-n" if platform.system().lower() == "windows" else "-c"

            command = ["ping", param, "1", host]
            if output is None:
                result = subprocess.call(command) == 0
            else:
                execute_result = shell(command)
                result = execute_result.output()

        return result

    def parse_ping_result(self, ping_result: list) -> dict:
        """
        Method which parses a ping result, and returns a dict
        Input: list with 5 lines from the result of a commandline ping
        Line 1 contains somehting like: 64 bytes from 127.0.0.1: icmp_seq=1 ttl=64 time=0.101 ms
        on success and:
        From n.n.n.n icmp_seq=1 Destination Host Unreachable
        on failure
        And this is the one we are interested in
        Output: dict listing the ttl, response_time, ping succeed or not
        """
        if isinstance(ping_result, list):
            the_line = ping_result[1]
            first_part = the_line.split()[0]
            response_status = False if first_part == "From" else True
            ttl = -1 if first_part == "From" else int(the_line.split()[5].split("=")[1])
            response_time = (
                -1 if first_part == "From" else float(the_line.split()[6].split("=")[1])
            )

        else:
            response_status = False
            response_time = -1
            ttl = -1
        return {
            "response_status": response_status,
            "response_time": response_time,
            "ttl": ttl,
        }
