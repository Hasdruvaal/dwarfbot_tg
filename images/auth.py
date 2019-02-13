class ImagesAuthData:
    """ Dummy credentials storage, for cache key generation purpose """
    def __init__(self, api_key, api_secret):
        self.creds = [api_key, api_secret]
