import telebot
import log
from SessionManager import SessionManager

import config
telebot.apihelper.proxy = {'https': config.proxy}
bot = telebot.TeleBot(config.token)

SessionManager.initialise()

def private(f):
    def decorator(message):
        if (message.chat.type == "private"):
            f(message)
        else:
            bot.reply_to(message, "This command is not supported in groups.")
    return decorator

def group(f):
    def decorator(message):
        if (message.chat.type == "group" or message.chat.type == "supergroup"):
            f(message)
        else:
            bot.reply_to(message, "This command is not supported in private.")
    return decorator

def authorise(f):
    def decorator(message):
        if (SessionManager.checkUser(message.from_user.id)):
            f(message)
        else:
            bot.reply_to(message, "First send '/authorise' to the bot in private")
    return decorator

@bot.message_handler(commands=['authorise'])
@private
def send_greeting(message):
    log.logi(message, "Greeting sent")
    if (message.chat.type == "private"):
        SessionManager.addUser(message.from_user.id, message.chat.id)
    bot.reply_to(message, "Greetings! The bot recognised you.")

@bot.message_handler(commands=['create_session'])
@group
@authorise
def create_session(message):
    log.logi(message, "Session creation")
    ok = SessionManager.createSession("Untitled", message.from_user.id, message.chat.id)
    if (ok):
        bot.reply_to(message, "Session is created")
    else:
        bot.reply_to(message, "Failed to create: there is one already created by you in this chat.")


@bot.message_handler(commands=['delete_session'])
@group
@authorise
def delete_session(message):
    log.logi(message, "Session deleting")
    ok = SessionManager.deleteSession(message.from_user.id, message.chat.id)
    if (ok):
        bot.reply_to(message, "Session successfully deleted")
    else:
        bot.reply_to(message, "Failed to delete: you probably don't have any here")

print("Starting the bot")
bot.polling()