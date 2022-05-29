class LoginException(Exception):
    def __init__(self, *args):
        super(LoginException, self).__init__(*args)


class UnknownCrawlerException(Exception):
    def __init__(self, *args):
        super(UnknownCrawlerException, self).__init__(*args)
