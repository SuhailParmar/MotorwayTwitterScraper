from json import dumps as convert


class Tweet:
    """
    There is a lot of noise in an original tweet, for the purpose of
    this application we only require a few key attributes.
    """

    def __init__(self, screen_name, created_at, id, payload):
        self.screen_name = screen_name
        self.created_at = created_at
        self.id = id
        self.payload = payload
        self.as_json = convert(self.__dict__)

    @staticmethod
    def to_tweet(tweets_dict_array):
        arr = []
        for tweet in tweets_dict_array:
            t = Tweet(screen_name=tweet['user']["screen_name"],
                      created_at=tweet["created_at"],
                      id=tweet["id"],
                      payload=tweet["text"])

            arr.append(t.as_json)

        return arr
