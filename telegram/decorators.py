from functools import wraps
from logging import info

from telegram import bot
from db.manager import user_manager


def private(f):
    @wraps(f)
    def decorator(message):
        if message.chat.type == 'private':
            f(message)
        else:
            bot.reply_to(message, 'This command is not supported in groups.')
    return decorator


def group(f):
    @wraps(f)
    def decorator(message):
        if message.chat.type == 'group' or message.chat.type == 'supergroup':
            f(message)
        else:
            bot.reply_to(message, 'This command is not supported in private.')
    return decorator


def authorize(f):
    @wraps(f)
    def decorator(message):
        if user_manager.get(message.from_user.id):
            user_manager.update_user(id=message.from_user.id,
                                    user_name=message.from_user.username,
                                    first_name=message.from_user.first_name,
                                    last_name=message.from_user.last_name)
            f(message)
        else:
            bot.reply_to(message, 'First send `/auth` to the bot in private')
    return decorator


def logging(func):
    @wraps(func)
    def decorator(message):
        info((message.text, func.__name__))
        func(message)
    return decorator
