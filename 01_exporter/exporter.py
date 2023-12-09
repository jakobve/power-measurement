import argparse
import time
import logging
import socket
import select
import json
import sys
import os

from power_measurement import PowerMeasurement
from power_metrics import update_metrics
from prometheus_client import start_http_server
from typing import Tuple

logger = logging.getLogger(__name__)

DEVICE_FETCH_DATA_INTERVAL_SECONDS = 3
DEVICE_FETCH_DATA_TIMEOUT_SECONDS = 5

# Prometheus target port specified in: OpenFaas-Edge-Cluster-2/ansible/roles/monitoring/files/manifest/power-exporter-daemonSet.yml
HTTP_SERVER_PORT = 8000

# Specified in: OpenFaas-Edge-Cluster-2/ansible/roles/monitoring/files/manifest/power-exporter-daemonSet.yml
# IP 127.0.0.1
# Port 5000
ENV_VAR_DEVICE_IP = 'DEVICE_UDP_IP'
ENV_VAR_DEVICE_PORT = 'DEVICE_UDP_PORT'



def get_device_ip_and_port() -> Tuple[str, int]:
    """
    Returns the IP and Port of the target device, either based on configured ENVs or command-line arguments.
    :return: a tuple composed of the IP and Port of the target device.
    """
    if len(sys.argv) == 1:
        logger.info("Trying to determine device IP and Port via ENVs ...")
        if ENV_VAR_DEVICE_IP not in os.environ or ENV_VAR_DEVICE_PORT not in os.environ:
            logger.error("ENVs '{}' and '{}' must be set when no arguments are given.".format(ENV_VAR_DEVICE_IP,
                                                                                              ENV_VAR_DEVICE_PORT))
            raise SystemExit(1)
        return os.environ[ENV_VAR_DEVICE_IP], int(os.environ[ENV_VAR_DEVICE_PORT])
    else:
        args = parse_args()
        logger.info("Successfully parsed the command-line arguments: {}".format(args))
    
        return args.device_ip, args.device_port


def parse_args() -> argparse.Namespace:
    """ Returns the parsed command-line arguments. """
    parser = argparse.ArgumentParser(description="Prometheus exporter designed for monitoring the power consumption of"
                                                 " edge-enabled IoT devices. The power-related data is fetched from the"
                                                 " device via UDP using protobuffers.")
    parser.add_argument("--device-ip", type=str, required=True, help="The IP of the target device.")
    parser.add_argument("--device-port", type=int, required=True, help="The Port of the target device to connect to.")

    return parser.parse_args()


def fetch_data(ip: str, port: int) -> None:
    """
    Starts to fetch data from the target device via UDP and updates the metrics accordingly.

    To this end, a request message is sent regularly before waiting for a corresponding
    response that is expected to contain the most recent data. Metrics are updated once a response was received.

    :param ip: the IP of the target device.
    :param port: the Port of the target device to connect to.
    """
    request_msg = str.encode("DATA_REQUEST")
    rx_buffer_size = 1024

    logger.info("Creating socket ...")
    sock = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
    logger.info("Successfully created socket.")

    logger.info("Starting UDP communication with target device (IP: {} | Port: {}) ...".format(ip, port))

    while True:
        sock.sendto(request_msg, (ip, port))

        ready = select.select([sock], [], [], DEVICE_FETCH_DATA_TIMEOUT_SECONDS)
        logger.info(ready)

        if ready[0]:
            rx_data, address = sock.recvfrom(rx_buffer_size)
            sender_ip, sender_port = address
            logger.info("Received {} bytes from {}:{}".format(len(rx_data), sender_ip, sender_port))

            received_json = rx_data.decode('utf-8')
            measurement_dict = json.loads(received_json)

            logger.info(measurement_dict)

            measurement = PowerMeasurement(
                timestamp = measurement_dict['timestamp'],
                device_energy_consumption_mw = measurement_dict['device_energy_consumption_mw'],
                device_energy_consumption_ma = measurement_dict['device_energy_consumption_ma'],
                energy_supply = measurement_dict['energy_supply'],
                battery_capacity_rel = measurement_dict['battery_capacity_rel']
                )

            update_metrics(measurement)
            time.sleep(DEVICE_FETCH_DATA_INTERVAL_SECONDS)
        else: 
            logger.warning("Timeout occured on socket recvfrom! Requesting data from target device again.")


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(name)s - %(levelname)s >>> %(message)s',
                        handlers=[logging.StreamHandler()])

    device_ip, device_port = get_device_ip_and_port()

    logger.info("Starting HTTP Server on Port {} ...".format(HTTP_SERVER_PORT))

    # HTTP server exposing the metrics ...
    start_http_server(HTTP_SERVER_PORT)

    # Fetch data and update metrics ...
    fetch_data(device_ip, device_port)
