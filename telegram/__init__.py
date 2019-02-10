import telebot

import config.bot as config

try:
    telebot.apihelper.proxy = config.proxy
except:
    pass

bot = telebot.TeleBot(config.token)

from telegram.decorators import *
from telegram.session import *
from telegram.user import *
from telegram.user_session import *
