from telebot import types

from telegram import bot
from telegram.decorators import *
from db.manager import SessionManager

hideBoard = types.ReplyKeyboardRemove()
chosen_sessions = {}


@bot.message_handler(commands=['create'])
@private # TODO: change to group, private for test only
@authorise
@logging
def create_session(message):
    name = ' '.join(message.text.split(maxsplit=1)[1:]).strip() or 'Untitled'
    if SessionManager.create_session(name, message.from_user.id, message.chat.id):
        bot.reply_to(message, "Session is created")
    else:
        bot.reply_to(message, "Failed to create: there is one already created by you in this chat.")


@bot.message_handler(commands=['delete'])
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
    name = ' '.join(message.text.split(maxsplit=1)[1:]).strip()
    if not name:
        return
    if SessionManager.rename_session(name, message.from_user.id, message.chat.id):
        bot.reply_to(message, 'Session was renamed!')
    else:
        bot.reply_to(message, 'Failed to rename: there is no session created by you in this chat.')


@bot.message_handler(commands=['description'])
@authorise
@private
@logging
def description(message):
    new_desc = ' '.join(message.text.split(maxsplit=1)[1:]).strip() or None
    desc = SessionManager.description(message.from_user.id, message.chat.id, new_desc)
    if desc and not new_desc:
        bot.reply_to(message, 'Session description: '+desc)
    if desc and new_desc:
        bot.reply_to(message, 'Session description changed!')
    elif new_desc and not desc:
        bot.reply_to(message, 'Failed to change description: there is no session created by you in this chat.')
