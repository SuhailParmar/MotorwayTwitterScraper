class Tweet:
    """
    There is a lot of noise in an original tweet, for the purpose of 
    this application we only require a few key attributes.
    """
    def __init__(self,screen_name, created_at, id, text):
        self.screen_name = screen_name
        self.created_at = created_at
        self.id = id
        self.payload = text