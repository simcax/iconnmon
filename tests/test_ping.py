"""
Tests for pinging and parsing the ping result
"""

import pytest

from iconnmon import check_hosts as ch


def test_ping_localhost():
    """
    Ping localhost and make sure a correct ip address will get a response
    """
    host = "127.0.0.1"
    result = ch.ping_host(host=host)
    assert result is True


def test_ping_localhost_full_result():
    """
    Ping localhost and receive the ping result
    """
    host = "127.0.0.1"
    result = ch.ping_host(host=host, output="full")
    assert isinstance(result, list)


def test_ip_address_failing():
    """
    Test a false when checking a wrong ip v4 address
    """
    address = "127.2222.1.1"
    assert ch._check_ip(address) is False


def test_ping_localhost_wrong_ip():
    """
    Make sure an invalid IP address will fail
    """
    host = "127.0.2222.1"
    assert ch.ping_host(host=host) is False
