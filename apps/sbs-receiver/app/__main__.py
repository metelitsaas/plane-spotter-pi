import os
import json
import pika
from utils.logger import logger
from utils.rabbit_client import RabbitClient
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
    rabbitmq_client = RabbitClient(rabbitmq_host, rabbitmq_port, rabbitmq_vhost, rabbitmq_user, rabbitmq_pass)
    rabbitmq_client.channel.exchange_declare(
        exchange=rabbitmq_exchange_name,
        exchange_type=rabbitmq_exchange_type,
        durable=True
    )

    # Get messages from receiver and send to broker
    for message in receiver.get_message():
        logger.info(f"Received message from aircraft hex id: {message['hex_ident']}")
        serialized_message = json.dumps(message)
        rabbitmq_client.channel.basic_publish(
            exchange=rabbitmq_exchange_name,
            routing_key='',
            body=serialized_message,
            properties=pika.BasicProperties(delivery_mode=2,)
        )


if __name__ == '__main__':
    main()
