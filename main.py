import twitter
import logging
import lib.config as config

from lib.logger import Logger
from lib.file_handler import FileHandler
from lib.twitter_handler import TwitterHandler
from lib.rabbitmq_client import RabbitMQClient
from lib.tweet import Tweet


main_logger = logging.getLogger("Main")
Logger.initiate_logger()


def main():
    th = TwitterHandler()
    fh = FileHandler()
    mq = RabbitMQClient()

    main_logger.info('Starting Tweet Scraping [account @{}]'.format
                     (config.twitter_handle))

    # Obtain the first tweet from the user and convert to an array of dicts
    tweets = th.get_tweets_from_user_as_dict()
    latest_tweet = tweets[0]

    if not fh.file_exists():
        # remove unnecessary json values
        tweet_arr = Tweet.to_tweet(tweets)
        mq.publish(tweet_arr)

    else:
        last_recorded_tweet_id = fh.read_id_from_file()
        if not th.is_recorded_tweet_id_same_as_latest(last_recorded_tweet_id):

            tweets_missing =\
                th.number_of_tweets_inbetween_last_recorded_and_last_tweeted(
                    last_recorded_tweet_id)

            tweets_dict_array =\
                th.get_tweets_from_user_as_dict(number=tweets_missing)

            tweet_arr = Tweet.to_tweet(tweets_dict_array)
            mq.publish(tweet_arr)

    main_logger.info('Finished Scraping.')

if __name__ == "__main__":
    main()
