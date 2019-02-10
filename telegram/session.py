from telebot import types

from telegram import bot
from telegram.decorators import *
from db.manager import SessionManager

hideBoard = types.ReplyKeyboardRemove()
chosen_sessions = {}


@bot.message_handler(commands=['create_session'])
@private # TODO: change to group, private for test only
@authorise
@logging
def create_session(message):
    name = ' '.join(message.text.split(maxsplit=1)[1:]) or 'Untitled'
    if SessionManager.create_session(name, message.from_user.id, message.chat.id):
        bot.reply_to(message, "Session is created")
    else:
        bot.reply_to(message, "Failed to create: there is one already created by you in this chat.")


@bot.message_handler(commands=['delete_session'])
@private
@authorise
@logging
def delete_session(message):
    if SessionManager.delete_session(message.from_user.id, message.chat.id):
        bot.reply_to(message, "Session is deleted")
    else:
        bot.reply_to(message, "Failed to delete: there is no sessions created by you in this chat.")


@bot.message_handler(commands=['name'])
@authorise
@private
@logging
def rename_session(message):
    name = ' '.join(message.text.split(maxsplit=1)[1:])
    if not name:
        return
    if SessionManager.rename_session(name, message.from_user.id, message.chat.id):
        bot.reply_to(message, 'Session was renamed!')
    else:
        bot.reply_to(message, 'Failed to rename: there is no session created by you in this chat.')

