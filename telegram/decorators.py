from functools import wraps
from logging import info

from telegram import bot
from db.manager import UserManager


def private(f):
    @wraps(f)
    def decorator(message):
        if message.chat.type == "private":
            f(message)
        else:
            bot.reply_to(message, "This command is not supported in groups.")
    return decorator


def group(f):
    @wraps(f)
    def decorator(message):
        if message.chat.type == "group" or message.chat.type == "supergroup":
            f(message)
        else:
            bot.reply_to(message, "This command is not supported in private.")
    return decorator


def authorise(f):
    @wraps(f)
    def decorator(message):
        if UserManager.check_user(message.from_user.id):
            f(message)
        else:
            bot.reply_to(message, "First send '/auth' to the bot in private")
    return decorator


def logging(f):
    @wraps(f)
    def decorator(message):
        info((message, f.__name__))
        f(message)
    return decorator
