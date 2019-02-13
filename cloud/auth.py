class CloudAuthData:
    """ Dummy credentials storage, for cache key generation purpose """
    def __init__(self, scopes, secret_file):
        self.scopes = scopes
        self.secret_file = secret_file

