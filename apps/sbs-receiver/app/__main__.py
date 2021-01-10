import os
import json
from utils.logger import logger
from rabbitmq.client import Client
from receiver import Receiver


# TODO: Add delay support in docker-compose

def main():

    # dump1090 environment
    dump1090_host = os.environ['DUMP1090_HOST']
    dump1090_port = os.environ['DUMP1090_PORT']

    # RabbiMQ environment
    rabbitmq_host = os.environ['RABBITMQ_HOST']
    rabbitmq_port = os.environ['RABBITMQ_PORT']
    rabbitmq_user = os.environ['RABBITMQ_USER']
    rabbitmq_pass = os.environ['RABBITMQ_PASS']
    rabbitmq_vhost = os.environ['RABBITMQ_VHOST']
    rabbitmq_exchange_name = os.environ['RABBITMQ_EXCHANGE_NAME']
    rabbitmq_exchange_type = os.environ['RABBITMQ_EXCHANGE_TYPE']

    # Set RTL-SDR receiver
    receiver = Receiver(dump1090_host, dump1090_port)

    # Set RabbitMQ producer
    rabbitmq_client = Client(rabbitmq_host, rabbitmq_port, rabbitmq_vhost, rabbitmq_user, rabbitmq_pass)
    channel = rabbitmq_client.get_channel()
    channel.exchange_declare(rabbitmq_exchange_name, rabbitmq_exchange_type)

    # Get messages from receiver and send to broker
    for message in receiver.get_message():
        logger.info(f"Received message from aircraft hex id: {message['hex_ident']}")
        serialized_message = json.dumps(message)
        channel.publish(serialized_message, rabbitmq_exchange_name)


if __name__ == '__main__':
    main()
