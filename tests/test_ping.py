"""
Tests for pinging and parsing the ping result
"""

import pytest

from iconnmon.check_hosts import IConnMonPing


def test_ping_localhost():
    """
    Ping localhost and make sure a correct ip address will get a response
    """
    host = "127.0.0.1"
    icm_ping = IConnMonPing()
    result = icm_ping.ping_host(host=host)
    assert result is True


def test_ping_localhost_full_result():
    """
    Ping localhost and receive the ping result
    """
    host = "127.0.0.1"
    icm_ping = IConnMonPing()
    result = icm_ping.ping_host(host=host, output="full")
    assert isinstance(result, list)


def test_ip_address_failing():
    """
    Test a false when checking a wrong ip v4 address
    """
    address = "127.2222.1.1"
    icm_ping = IConnMonPing()
    assert icm_ping._check_ip(address) is False


def test_ping_localhost_wrong_ip():
    """
    Make sure an invalid IP address will fail
    """
    icm_ping = IConnMonPing()
    host = "127.0.2222.1"
    assert icm_ping.ping_host(host=host) is False


def test_parse_ping_response_success():
    """
    Test we are able to get ttl, response time and if the ping succeeded
    """
    icm_ping = IConnMonPing()
    host = "127.0.0.1"
    # result = icm_ping.ping_host(host=host, output="full")
    result = [
        "PING 127.0.0.1 (127.0.0.1) 56(84) bytes of data.",
        "64 bytes from 127.0.0.1: icmp_seq=1 ttl=64 time=0.060 ms",
        "--- 127.0.0.1 ping statistics ---",
        "1 packets transmitted, 1 received, 0% packet loss, time 0ms",
        "rtt min/avg/max/mdev = 0.060/0.060/0.060/0.000 ms",
    ]
    parsed_result = icm_ping.parse_ping_result(result)
    assert isinstance(parsed_result, dict)
    assert parsed_result.get("ttl") == 64
    assert parsed_result.get("response_time") == 0.060
    assert parsed_result.get("response_status")


def test_parse_ping_response_failed():
    """
    Test we are able to get ttl, response time and if the ping succeeded
    """
    icm_ping = IConnMonPing()
    host = "172.20.20.161"
    # result = icm_ping.ping_host(host=host, output="full")
    result = [
        "PING 10.1.1.1 (10.1.1.1) 56(84) bytes of data.",
        "From 10.1.1.1 icmp_seq=1 Destination Host Unreachable",
        "--- 10.1.1.1 ping statistics ---",
        "1 packets transmitted, 0 received, +1 errors, 100% packet loss, time 0ms",
    ]
    parsed_result = icm_ping.parse_ping_result(result)
    assert isinstance(parsed_result, dict)
    assert parsed_result.get("ttl") == -1
    assert parsed_result.get("response_time") == -1
    assert parsed_result.get("response_status") is False
