import logging
from time import sleep
from json import loads

import lib.config as config
from lib.logger import Logger
from lib.file_handler import FileHandler
from lib.twitter_handler import TwitterHandler
from lib.rabbitmq_client import RabbitMQClient
from lib.tweet import Tweet

scraper_logger = logging.getLogger("TweetScraper")
Logger.initiate_logger()


class Scraper:

    def __init__(self):
        self.th = TwitterHandler()
        self.fh = FileHandler()
        self.mq = RabbitMQClient()
        # NONE shows the scraper hasn't been run
        self.last_recorded_tweet_id = None

    def scrape(self):
        scraper_logger.info(
            'Scraping account @{0}'.format(config.twitter_handle))

        latest_tweet = self.th.get_tweets_from_user_as_dict(number=1)[0]
        latest_tweet_id = self.th.extract_id(latest_tweet)
        scraper_logger.debug(
            'Scraped ID: {0}'.format(latest_tweet_id))

        if self.last_recorded_tweet_id is None:
            # First time the Scraper is run so populate the last_recorded_tweet_id
            if self.fh.file_exists():
                self.last_recorded_tweet_id = self.fh.read_id_from_file()
                scraper_logger.info('Last recorded tweet ID found: {}'.format
                                    (self.last_recorded_tweet_id))
            else:
                scraper_logger.warn('Tool has no knowledge of a previous tweet')
                self.last_recorded_tweet_id = False

        if self.last_recorded_tweet_id is False:
            latest_tweet = Tweet.to_tweet([latest_tweet])
            self.mq.publish(latest_tweet)
            self.fh.write_id_to_file(latest_tweet_id)
            self.last_recorded_tweet_id = latest_tweet_id
            return

        # Check if the latest_tweet as already been scraped by the tool
        if self.th.is_recorded_tweet_id_same_as_latest(
                self.last_recorded_tweet_id, latest_tweet_id):

            scraper_logger.info(
                'Tweet {} has already been scraped.'.format(latest_tweet_id))
            return

        # As we are unsure about the fq of the tweets from the account
        # We always see if tweets are missing between Last recorded and latest
        scraper_logger.info('There may tweets not captured by this tool.')
        tweets_missing =\
            self.th.number_of_tweets_inbetween_last_recorded_and_last_tweeted(
                self.last_recorded_tweet_id)

        tweet_arr = Tweet.to_tweet(tweets_missing)
        self.mq.publish(tweet_arr)

        # The first tweet in array was tweeted the most recently
        tweet_json = loads(tweet_arr[0])
        self.fh.write_id_to_file(id=tweet_json["id"])
        self.last_recorded_tweet_id = tweet_json["id"]