import pika
import config
import logging

mq_logger = logging.getLogger("RMQ")

class RabbitMQClient:

    def __init__(self):
        self.username = config.rabbit_username
        self.password = config.rabbit_password
        self.host = config.rabbit_host
        self.port = config.rabbit_port
        self.queue = config.rabbit_queue
        self.exchange = config.rabbit_exchange
        self.routing_key = config.rabbit_routing_key
        self.vhost = config.rabbit_vhost

    def connect_to_mq(self):

        credentials = pika.PlainCredentials(self.username, self.password)
        parameters = pika.ConnectionParameters(
            self.host, int(self.port), self.vhost, credentials, ssl=False)

        connection = pika.BlockingConnection(parameters)
        return connection
    
    def publish(self, payload):
        
        channel = self.connect_to_mq().channel()
        channel.basic_publish(self.exchange,
                            self.routing_key,
                            payload,
                            pika.BasicProperties(content_type='application/json',
                                                delivery_mode=1))
        
        mq_logger.info('Published a message to {}'.format(self.queue))
        channel.close()
