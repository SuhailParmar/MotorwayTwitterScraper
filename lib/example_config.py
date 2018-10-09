from os import getenv

# Twitter Specific Values
twitter_handle = getenv("TWITTER_HANDLE", "Traffic_M6")
access_token = getenv("ACCESS_TOKEN",
                      "XXX")
access_token_secret = getenv("ACCESS_TOKEN_SECRET",
                             "XXX")
api_key = getenv("API_KEY", "XXX")
api_secret = getenv(
    "API_SECRET", "XXX")

# Rabbit Specific Values
rabbit_host = getenv("MQ_HOST", "localhost")
rabbit_port = getenv("MQ_PORT", 5672)
rabbit_queue = getenv("MQ_QUEUE", "XXX")
rabbit_username = getenv("MQ_USERNAME", "XXX")
rabbit_password = getenv("MQ_PASSWORD", "XXX")
rabbit_exchange = getenv("MQ_EXCHANGE", "XXX")
rabbit_routing_key = getenv("MQ_ROUTING_KEY", "XXX")
rabbit_vhost = getenv("MQ_VHOST", "XXX")

# Application Specific Values
last_tweet_id_filename = getenv("FILENAME", "XXX")
log_file = getenv("LOG_FILE", "mtw.log")
