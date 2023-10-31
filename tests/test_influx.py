"""
Tests around inserting data in influxdb
"""

import os
import time

import influxdb_client
from dotenv import load_dotenv
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS
from shell import shell

from iconnmon.check_hosts import IConnMonPing
from iconnmon.register import IConnMonnRegister


def test_influx_insert_data():
    """
    Initial test to add data to influxdb
    """
    load_dotenv()
    token = os.environ.get("INFLUXDB_TOKEN")
    org = "iconnmon"
    url = "http://localhost:8086"
    bucket = "iconnmonseries"
    iconn_reg = IConnMonnRegister(token=token, org=org, url=url, bucket=bucket)
    result = iconn_reg.register_point(
        host="127.0.0.1", ttl=64, response_time=0.101, status=True
    )
    assert result


def test_influx_insert_data_wrong_token():
    """
    Initial test to add data to influxdb
    """
    load_dotenv()
    token = "notTheRealToken"
    org = "iconnmon"
    url = "http://localhost:8086"
    bucket = "iconnmonseries"
    iconn_reg = IConnMonnRegister(token=token, org=org, url=url, bucket=bucket)
    result = iconn_reg.register_point(
        host="127.0.0.1", ttl=64, response_time=0.101, status=True
    )
    assert result is False


def test_insert_data_in_influx():
    """
    Initial test to add data to influxdb
    """
    load_dotenv()
    token = os.environ.get("INFLUXDB_TOKEN")
    org = "iconnmon"
    url = "http://localhost:8086"
    bucket = "iconnmonseries"
    iconn_reg = IConnMonnRegister(token=token, org=org, url=url, bucket=bucket)
    outcome = True
    for value in range(50):
        result = iconn_reg.register_point(
            host="127.0.0.1", ttl=64, response_time=0.101, status=True
        )
        if result:
            time.sleep(1)
        else:
            outcome = False
    assert outcome


def test_add_ping_data_in_influx():
    """
    Test to adding data to influxdb
    """
    load_dotenv()
    token = os.environ.get("INFLUXDB_TOKEN")
    org = "iconnmon"
    url = "http://localhost:8086"
    bucket = "iconnmonseries"
    iconn_reg = IConnMonnRegister(token=token, org=org, url=url, bucket=bucket)
    icm_ping = IConnMonPing()
    host = "127.0.0.1"

    outcome = True
    for value in range(50):
        response = icm_ping.ping_host(host=host, output="full")
        result = icm_ping.parse_ping_result(response)
        ping_result = iconn_reg.register_point(
            host=host,
            status=result.get("response_status"),
            ttl=result.get("ttl"),
            response_time=result.get("response_time"),
        )
        if ping_result:
            time.sleep(1)
        else:
            outcome = False
    assert outcome
