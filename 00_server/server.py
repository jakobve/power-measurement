import time
import logging
import socket
import jsonpickle
import concurrent.futures
import traceback
from energy_management_system import EnergyManagementSystem

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s >>> %(message)s',
    handlers=[logging.StreamHandler()]
    )
logger = logging.getLogger(__name__)

logger.info("Starting server")

# Target to be requested by exporter
localIP = "0.0.0.0"
localPort = 5000
bufferSize = 1024

msgFromServer = "Hello UDP Client"
bytesToSend = str.encode(msgFromServer)

UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
logger.info("Created socket")

UDPServerSocket.bind((localIP, localPort))
logger.info("UDP server up and listening on {}, {}".format(localIP, localPort))

def get_powermeasurement(energy_management_system: EnergyManagementSystem):
    # Enqueue the power measurement request
    measurement = energy_management_system.get_powermeasurement()

    if measurement is not None:
        measurement_json = jsonpickle.encode(measurement)
        return str.encode(measurement_json)
    else:
        return str.encode("Measurement is None")


def start_server(energy_management_system: EnergyManagementSystem):
    try:
        while True:
            logger.info("Server running")
            bytesAddressPair = UDPServerSocket.recvfrom(bufferSize)
            logger.info("Message received")

            message = bytesAddressPair[0]
            unicode_message = message.decode("utf-8")

            address = bytesAddressPair[1]

            if unicode_message == "DATA_REQUEST":
                logger.info("+++++++++++++++++++++++++ Data request ++++++++++++++++++++++++")

                bytesToSend = get_powermeasurement(energy_management_system)
                logger.info(bytesToSend)
                # Sending a reply to client
                UDPServerSocket.sendto(bytesToSend, address)

            logger.info("Message from Client ({}):{}".format(address, unicode_message))

            time.sleep(1)

    except Exception as e:
        # Log the exception details
        logger.error(f"Error in server loop: {e}")
        traceback.print_exc() 

if __name__ == '__main__':
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:

        energy_manager = EnergyManagementSystem()
        future1 = executor.submit(energy_manager.manage)
        future2 = executor.submit(start_server, energy_manager)
        
        
