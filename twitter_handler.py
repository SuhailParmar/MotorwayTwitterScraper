import config
import twitter
import logging
from sys import exit
from file_handler import FileHandler

th_logger = logging.getLogger("TwitterHandler")


class TwitterHandler:

    def __init__(self):
        self.api = self.authenticate()

    def authenticate(self):
        return twitter.Api(consumer_key=config.API_KEY,
                           consumer_secret=config.API_SECRET,
                           access_token_key=config.ACCESS_TOKEN,
                           access_token_secret=config.ACCESS_TOKEN_SECRET)

    def extract_id(self, tweet):
        return int(tweet['id'])

    def extract_created_at(self, tweet):
        return tweet['created_at']

    def extract_time_from_created_at(self, created_at):
        a = created_at.split()
        return a[3]

    def get_tweets_from_user_as_dict(self, handle=config.M6_TWITTER_HANDLE, number=1):

        try:
            tweets = self.api.GetUserTimeline(screen_name=handle, count=number)
            th_logger.debug('Scraped {} users tweets.'.format(len(tweets)))
        except Exception as e:
            th_logger.error(e)
            exit(1)
        
        arr = []
        for tweet in tweets:
            arr.append(tweet.AsDict())
        return arr

    def is_recorded_tweet_id_same_as_latest(self, recorded_id):
        # Get the latest tweet from the user
        # compare it with the latest recorded id
        tweets = self.get_tweets_from_user_as_dict(number=1)
        latest_tweet = tweets[0]

        latest_tweet_id = self.extract_id(latest_tweet)
        return (recorded_id == latest_tweet_id)

    def number_of_tweets_inbetween_last_recorded_and_last_tweeted(self, recorded_id):
        i = 0
        while i < 100:
            tweets = self.get_tweets_from_user_as_dict(number=i+1)
            latest_id = self.extract_id(tweets[i])
            if latest_id == recorded_id:
                th_logger.info('Found {} unrecorded tweet(s)!'.format(i))
                return i
            i += 1

        th_logger.error(
            'There could be more than {} tweet(s) missing...'.format(i))
        exit(1)
