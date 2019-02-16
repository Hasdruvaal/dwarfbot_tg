import datetime
import telebot

import config.telegram as config

try:
    telebot.apihelper.proxy = config.proxy
except:
    pass

bot = telebot.TeleBot(config.token)

from telegram.decorators import *
from telegram.session import *
from telegram.user import *
from telegram.user_session import *
from telegram.save import *


next_check = datetime.datetime.now()

@bot.message_handler(func=lambda x: datetime.datetime.now() > next_check)
def skip_sleepers(message):
    sleepers = userSessionManager.sleepers()
    if sleepers:
        next_check = datetime.datetime.now() + datetime.timedelta(hours=5)
        info('Sleepers gonna sleep!')
        for sleeper in sleepers:
            message.chat.id = sleeper.session.chat
            skip_player(message)
