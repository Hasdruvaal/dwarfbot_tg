import datetime
import telebot

import config

try:
    telebot.apihelper.proxy = config.tg_proxy
except:
    pass

bot = telebot.TeleBot(config.tg_token)

from telegram.decorators import *
from telegram.session import *
from telegram.user import *
from telegram.user_session import *
from telegram.save import *
from telegram.info import *


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
