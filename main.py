import twitter
import config
import threading
import logging
from logger import Logger
from file_handler import FileHandler
from twitter_handler import TwitterHandler
from rabbitmq_client import RabbitMQClient
from tweet import Tweet

main_logger = logging.getLogger("Main")


def main():

    th = TwitterHandler()
    fh = FileHandler()
    mq = RabbitMQClient()

    Logger.initiate_logger()

    main_logger.info('Starting poll...')
    threading.Timer(30, main).start()

    # Grab the latest Tweet
    tweets = th.get_tweets_from_user_as_dict()
    latest_tweet = tweets[0]

    # Inspect the tweet's id with the one from record
    if not fh.file_exists():
        latest_tweet_id = th.extract_id(latest_tweet)
        fh.write_to_text_file(latest_tweet_id)

        # remove unnecessary json values
        tweet_arr = Tweet.to_tweet(tweets)
        mq.publish(tweet_arr)

    else:
        last_recorded_tweet_id = fh.read_from_text_file()

        if not th.is_recorded_tweet_id_same_as_latest(last_recorded_tweet_id):

            tweets_missing =\
                th.number_of_tweets_inbetween_last_recorded_and_last_tweeted(
                    last_recorded_tweet_id)

            tweets_dict_array =\
                th.get_tweets_from_user_as_dict(number=tweets_missing)

            tweet_arr = Tweet.to_tweet(tweets_dict_array)
            mq.publish(tweet_arr)
    
    main_logger.info('Finished poll.')


if __name__ == "__main__":
    Logger.initiate_logger()
    while True:
        main()
