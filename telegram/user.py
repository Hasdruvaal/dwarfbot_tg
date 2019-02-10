from telegram import bot
from telegram.decorators import *
from db.manager import UserManager


@bot.message_handler(commands=['auth'])
@private
@logging
def send_greeting(message):
    if message.chat.type == "private":
        UserManager.add_user(message.from_user.id,
                             message.chat.id,
                             message.from_user.username,
                             message.from_user.first_name,
                             message.from_user.last_name
                             )
    bot.reply_to(message, "Greetings! The bot recognised you.")
