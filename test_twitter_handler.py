from twitter_handler import TwitterHandler
from file_handler import FileHandler

class TestTwitterHandlerTests:

    fh = FileHandler()
    th = TwitterHandler()

    def test_get_tweets_from_user_as_dict(self):
        dic = self.th.get_tweets_from_user_as_dict(number=2)
        assert len(dic) == 2
        assert isinstance(dic[0], dict)
        assert isinstance(dic[1], dict)
        assert dic[0]["id"]
        assert dic[1]["id"]

    def test_extract_id(self):
        assert self.th.extract_id({"id": 12}) == 12

    def test_is_recorded_tweet_same_as_latest(self):
        # Mocking out reading the id from file
        tweets = self.th.get_tweets_from_user_as_dict(number=2)
        recorded_tweet_id = self.th.extract_id(tweets[1])

        assert self.th.is_recorded_tweet_id_same_as_latest(recorded_tweet_id) is False

    def test_is_new_tweet_is_false(self):
        # Mocking out reading the id from file
        tweets = self.th.get_tweets_from_user_as_dict(number=2)
        recorded_tweet_id = self.th.extract_id(tweets[0])

        assert self.th.is_recorded_tweet_id_same_as_latest(recorded_tweet_id) is True


    def test_one_more_tweets_since_last_recorded(self):
        # Mocking out reading the id from file
        tweets = self.th.get_tweets_from_user_as_dict(number=2)
        recorded_tweet_id = self.th.extract_id(tweets[len(tweets)-1])

        a = self.th.number_of_tweets_inbetween_last_recorded_and_last_tweeted(recorded_tweet_id)
        assert a == 1

    def test_two_more_tweets_since_last_recorded(self):
        # Mocking out reading the id from file
        tweets = self.th.get_tweets_from_user_as_dict(number=3)
        recorded_tweet_id = self.th.extract_id(tweets[len(tweets)-1])

        a = self.th.number_of_tweets_inbetween_last_recorded_and_last_tweeted(recorded_tweet_id)
        assert a == 2

    def test_ten_more_tweets_since_last_recorded(self):
        # Mocking out reading the id from file
        tweets = self.th.get_tweets_from_user_as_dict(number=11)
        recorded_tweet_id = self.th.extract_id(tweets[len(tweets)-1])

        a = self.th.number_of_tweets_inbetween_last_recorded_and_last_tweeted(recorded_tweet_id)
        assert a == 10

        


