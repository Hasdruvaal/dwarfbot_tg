from functools import wraps

import telebot
from telebot import types

import log
from SessionManager import SessionManager, User, Session

import config

try:
    telebot.apihelper.proxy = {'https': config.proxy}
except:
    pass
bot = telebot.TeleBot(config.token)

SessionManager.initialise()
hideBoard = types.ReplyKeyboardRemove()


def private(f):
    @wraps(f)
    def decorator(message):
        if (message.chat.type == "private"):
            f(message)
        else:
            bot.reply_to(message, "This command is not supported in groups.")

    return decorator


def group(f):
    @wraps(f)
    def decorator(message):
        if (message.chat.type == "group" or message.chat.type == "supergroup"):
            f(message)
        else:
            bot.reply_to(message, "This command is not supported in private.")

    return decorator


def authorise(f):
    @wraps(f)
    def decorator(message):
        if (SessionManager.checkUser(message.from_user.id)):
            f(message)
        else:
            bot.reply_to(message, "First send '/authorise' to the bot in private")

    return decorator


def logging(f):
    @wraps(f)
    def decorator(message):
        if (SessionManager.checkUser(message.from_user.id)):
            log.logi(message, f.__name__)
            f(message)
        else:
            bot.reply_to(message, "First send '/authorise' to the bot in private")

    return decorator


@bot.message_handler(commands=['authorise'])
@private
@logging
def send_greeting(message):
    if (message.chat.type == "private"):
        SessionManager.addUser(message.from_user.id, message.chat.id)
    bot.reply_to(message, "Greetings! The bot recognised you.")


@bot.message_handler(commands=['create_session'])
@group
@authorise
@logging
def create_session(message):
    ok = SessionManager.createSession("Untitled", message.from_user.id, message.chat.id)
    if (ok):
        bot.reply_to(message, "Session is created")
    else:
        bot.reply_to(message, "Failed to create: there is one already created by you in this chat.")


@bot.message_handler(commands=['delete_session'])
@group
@authorise
@logging
def delete_session(message):
    ok = SessionManager.deleteSession(message.from_user.id, message.chat.id)
    if (ok):
        bot.reply_to(message, "Session successfully deleted")
    else:
        bot.reply_to(message, "Failed to delete: you probably don't have any here")

print("Starting the bot")
bot.polling()
