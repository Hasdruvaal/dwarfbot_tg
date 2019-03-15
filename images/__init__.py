import config
from images.auth import ImagesAuthData
from images.session import ImageSession

auth_data = ImagesAuthData(config.imgur_key, config.imgur_secret)
client = ImageSession.imgur(auth_data)
