from imgurpython import ImgurClient
from images.auth import ImagesAuthData
from utils.cache import cached


class ImageSession(ImgurClient):
    def album(self, name, description):
        params = {
            'title': name,
            'description': description,
        }
        return self.create_album(params)


    @staticmethod
    @cached
    def imgur(creds: ImagesAuthData):
        client = ImageSession(*creds.creds)
        authorization_url = client.get_auth_url('pin')
        pin = input(authorization_url+'\nEnter pin code: ')
        credentials = client.authorize(pin, 'pin')
        client.set_user_auth(credentials['access_token'], credentials['refresh_token'])
        return client
