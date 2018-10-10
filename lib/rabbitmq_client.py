import pika
import logging
from json import dumps, loads
from sys import exit
import lib.config as config
from lib.file_handler import FileHandler

mq_logger = logging.getLogger("RabbitMqClient")


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
        self.type = 'application/json'

    def connect_to_mq(self):
        mq_logger.info('Connecting to mq...')
        credentials = pika.PlainCredentials(self.username, self.password)
        parameters = pika.ConnectionParameters(
            self.host, int(self.port), self.vhost, credentials, ssl=False)

        try:
            connection = pika.BlockingConnection(parameters)
            mq_logger.info('Successfully connected to rabbit.')
        except Exception as e:
            mq_logger.error(e)
            exit(1)

        return connection

    def publish(self, tweets):
        """
        @tweets - An Array of one or many tweets as json, see Tweet.to_tweet()
        """
        channel = self.connect_to_mq().channel()
        mq_logger.info(
            'Attempting to publish {} tweet(s) to rabbit.'.format(len(tweets)))
        for tweet in tweets:

            try:
                channel.basic_publish(self.exchange,
                                      self.routing_key,
                                      tweet,
                                      pika.BasicProperties(content_type=self.type,
                                                           delivery_mode=1))
                mq_logger.info(
                    'Published Message:{0} to queue:{1}'.format(tweet, self.queue))

            except Exception as e:
                mq_logger.error(e)
                exit(1)

        if len(tweets) > 0:
            # The array is sorted in descending created_at order
            fh = FileHandler()
            tweet_json = loads(tweets[0])
            fh.write_id_to_file(id=tweet_json["id"])

        channel.close()
