import twitter
import logging
from sys import exit
import lib.config as config
from lib.file_handler import FileHandler

th_logger = logging.getLogger("TwitterHandler")


class TwitterHandler:

    def __init__(self):
        self.api = self.authenticate()

    def authenticate(self):
        return twitter.Api(consumer_key=config.api_key,
                           consumer_secret=config.api_secret,
                           access_token_key=config.access_token,
                           access_token_secret=config.access_token_secret)

    def extract_id(self, tweet):
        return int(tweet['id'])

    def extract_created_at(self, tweet):
        return tweet['created_at']

    def extract_time_from_created_at(self, created_at):
        a = created_at.split()
        return a[3]

    def get_tweets_from_user_as_dict(self, handle=config.twitter_handle, number=1):
        """
        Tweets are in string json format
        Tweets need to be returned as a pydict
        """
        try:
            tweets = self.api.GetUserTimeline(
                screen_name=handle, count=number, include_rts=False)
        except Exception as e:
            th_logger.error(e)
            exit(1)

        th_logger.debug('Scraped {} tweets from user.'.format(len(tweets)))
        th_logger.debug(
            'Converting {} tweets into python dictionary.'.format(len(tweets)))

        arr = []
        for tweet in tweets:
            arr.append(tweet.AsDict())
        return arr

    @staticmethod
    def is_recorded_tweet_id_same_as_latest(recorded, latest):
        return (recorded == latest)

    def number_of_tweets_inbetween_last_recorded_and_last_tweeted(self, recorded_id):
        n = 5  # Number of tweets to grab at one time
        i = 0  # Index of the tweets array

        tweets = None
        while i < 100:
            tweets = self.get_tweets_from_user_as_dict(number=i+n)
            # API only allows for scraping of n events not n-x
            # We will recieve the tweets validated by the previous loop
            # Therefore only validate unvalidated tweets
            unvalidated_tweets = tweets[i:]

            for ind, tweet in enumerate(unvalidated_tweets):
                tweet_id = self.extract_id(tweet)
                if tweet_id == recorded_id:
                    # Calculate the tweet before the last recorded
                    slice_val = (len(tweets) - (n - ind))
                    tweets = tweets[:slice_val]
                    # Prevents sending duplicate events
                    th_logger.info('Found {} unrecorded tweet(s)!'.format
                                   (len(tweets)))
                    return tweets

            i += n

        th_logger.warning(
            'There could be more than {} tweet(s) missing...'.format(i))

        th_logger.warning(
            'Scraping {} tweets regardless.'.format(i))

        return tweets
