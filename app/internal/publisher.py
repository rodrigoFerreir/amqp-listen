from typing import Dict
import json
from . import *


class RabbitmqPublisher:
    def __init__(self, connection:ConnectionRabbitmq) -> None:
        self.connection = connection
        self.__channel = self.__create_channel()

    def __create_channel(self):
        connection_parameters = pika.ConnectionParameters(
            host= self.connection.host,
            port= self.connection.port,
            credentials= pika.PlainCredentials(
                username=self.connection.username,
                password=self.connection.password
            )
        )

        channel = pika.BlockingConnection(connection_parameters).channel()
        return channel

    def send_message(self, body: Dict):
        self.__channel.basic_publish(
            exchange=self.connection.exchange,
            routing_key=self.connection.routing_key,
            body=json.dumps(body),
            properties=pika.BasicProperties(
                delivery_mode=2
            )
        )
