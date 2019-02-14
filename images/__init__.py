from config import imgur as config
from images.auth import ImagesAuthData
from images.session import ImageSession

authData = ImagesAuthData(config.api_key, config.api_secret)
client = ImageSession.imgur(authData)
