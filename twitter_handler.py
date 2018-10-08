import config
import twitter
import logging
from file_handler import FileHandler


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
        tweets = self.api.GetUserTimeline(screen_name=handle, count=number)
        arr = []
        for tweet in tweets:
            arr.append(tweet.AsDict())
        return arr

    def is_recorded_tweet_id_same_as_latest(self,recorded_id):
        # Get the latest tweet from the user
        # compare it with the latest recorded id 
        tweets = self.get_tweets_from_user_as_dict(number=1)
        latest_tweet = tweets[0]

        latest_tweet_id = self.extract_id(latest_tweet)
        return (recorded_id == latest_tweet_id)

    def number_of_tweets_inbetween_last_recorded_and_last_tweeted(self, recorded_id):
        i = 0
        while i < 30:
            tweets = self.get_tweets_from_user_as_dict(number=i+1)
            if self.extract_id(tweets[i]) == recorded_id:
                return i # return the difference
            i+=1

        logging.warn('There could be more than {} tweets missing...'.format(i))
        return False
