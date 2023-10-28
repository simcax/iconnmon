"""
Module to register data in influxdb
"""

import influxdb_client
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS
from loguru import logger


class IConnMonnRegister:
    """
    Class to interact with InfluxDB
    """

    def __init__(self, org: str, token: str, url: str, bucket: str) -> None:
        self.org = org
        self.token = token
        self.url = url
        self.bucket = bucket
        write_client = influxdb_client.InfluxDBClient(url=url, token=token, org=org)
        self.write_api = write_client.write_api(write_options=SYNCHRONOUS)

    def register_point(
        self, host: str, status: bool, ttl: int, response_time: float
    ) -> bool:
        """
        Register a ping with ttl and response time in influx
        """
        point = (
            Point("ping")
            .tag("host", host)
            .field("response", status)
            .field("ttl", ttl)
            .field("response_time", response_time)
        )
        try:
            self.write_api.write(bucket=self.bucket, org=self.org, record=point)
            return True
        except Exception as error_text:
            logger.error(error_text)
            return False
