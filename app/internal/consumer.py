from . import *


class RabbitmqConsumer:
    def __init__(self, connection:ConnectionRabbitmq, callback) -> None:
        self.connection = connection
        self.__queue = "teste"
        self.__callback = callback
        self.__channel = self.__create_channel()

    def __create_channel(self):
        connection_parameters = pika.ConnectionParameters(
            host=self.connection.host,
            port=self.connection.port,
            credentials=pika.PlainCredentials(
                username=self.connection.username,
                password=self.connection.password
            )
        )

        channel = pika.BlockingConnection(connection_parameters).channel()
        channel.queue_declare(
            queue=self.__queue,
            durable=True
        )
        channel.basic_consume(
            queue=self.__queue,
            auto_ack=True,
            on_message_callback=self.__callback
        )

        return channel
    
    def start(self):
        print(f'Listen RabbitMQ on Port 5672')
        self.__channel.start_consuming()