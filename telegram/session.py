from telegram import bot
from telegram.decorators import *
from db.manager import sessionManager


@bot.message_handler(commands=['create'])
@group
@authorise
@logging
def create_session(message):
    name = ' '.join(message.text.split(maxsplit=1)[1:]).strip() or 'Untitled'
    if sessionManager.create_session(name, message.from_user.id, message.chat.id):
        bot.reply_to(message, "Session created")
    else:
        bot.reply_to(message, "Failed to create: there is a session already created by you in this chat.")


@bot.message_handler(commands=['delete'])
@group
@authorise
@logging
def delete_session(message):
    if sessionManager.delete_session(message.from_user.id, message.chat.id):
        bot.reply_to(message, "Session deleted")
    else:
        bot.reply_to(message, "Failed to delete: there are no sessions created by you in this chat.")


@bot.message_handler(commands=['name'])
@group
@authorise
@logging
def rename_session(message):
    new_name = ' '.join(message.text.split(maxsplit=1)[1:]).strip()
    name = sessionManager.rename(message.from_user.id, message.chat.id, new_name)
    if name:
        bot.reply_to(message, 'Session name: '+name)
    elif new_name and not name:
        bot.reply_to(message, 'Failed to change name: there is no session created by you in this chat.')
    else:
        bot.reply_to(message, 'There is nothing to show')


@bot.message_handler(commands=['description'])
@group
@logging
def description(message):
    new_desc = ' '.join(message.text.split(maxsplit=1)[1:]).strip() or None
    desc = sessionManager.description(message.from_user.id, message.chat.id, new_desc)
    if desc:
        bot.reply_to(message, 'Session description: '+desc)
    elif new_desc and not desc:
        bot.reply_to(message, 'Failed to change description: there is no session created by you in this chat.')
    else:
        bot.reply_to(message, 'There is nothing to show')


@bot.message_handler(commands=['start', 'embark'])
@authorise
@group
@logging
def start_session(message):
    session = sessionManager.active_chat_session(message.chat.id)
    if not session or session.status:
        return
    if session.id not in sessionManager.get_player_sessions(message.from_user.id):
        return

    if sessionManager.start(session.id):
        bot.reply_to(message, 'Strike the earth!')
    else:
        bot.reply_to(message, 'You are not prepared for a journey!')


@bot.message_handler(commands=['stop', 'abandon'])
@authorise
@group
@logging
def stop_session(message):
    session = sessionManager.active_chat_session(message.chat.id)
    if not session:
        return
    if session.id not in sessionManager.get_player_sessions(message.from_user.id):
        return

    if sessionManager.stop(session.id):
        bot.reply_to(message, 'Session was stopped')
    else:
        bot.reply_to(message, 'There is nothing to stop')
