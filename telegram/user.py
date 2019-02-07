from telegram import bot
from telegram.decorators import *
from db.models import SessionManager


@bot.message_handler(commands=['authorise'])
@private
@logging
def send_greeting(message):
    if message.chat.type == "private":
        SessionManager.addUser(message.from_user.id, message.chat.id)
    bot.reply_to(message, "Greetings! The bot recognised you.")
