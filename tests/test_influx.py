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

from iconnmon.register import IConnMonnRegister


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

    for value in range(500):
        iconn_reg.register_point(
            host="127.0.0.1", ttl=64, response_time=0.101, status=True
        )
        # point = Point("ping").tag("host", "127.0.0.1").field("response", True)
        # result = write_api.write(bucket=bucket, org=org, record=point,)
        time.sleep(1)


def test_retrieve_influx_token():
    """
    Test to retrive a token from influxdb
    """
    pass
