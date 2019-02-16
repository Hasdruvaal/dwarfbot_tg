import config
from images.auth import ImagesAuthData
from images.session import ImageSession

authData = ImagesAuthData(config.imgur_key, config.imgur_secret)
client = ImageSession.imgur(authData)
