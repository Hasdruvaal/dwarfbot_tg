from telegram import bot
from telegram.decorators import *
from db.manager import UserManager


@bot.message_handler(commands=['auth'])
@private
@logging
def send_greeting(message):
    if message.chat.type == "private":
        UserManager.add_user(message.from_user.id, message.chat.id)
    bot.reply_to(message, "Greetings! The bot recognised you.")
