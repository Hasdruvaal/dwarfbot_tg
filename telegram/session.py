from telegram import bot
from telegram.decorators import *
from db.manager import session_manager


@bot.message_handler(commands=['create'])
@group
@authorize
@logging
def create_session(message):
    name = ' '.join(message.text.split(maxsplit=1)[1:]).strip() or 'Untitled'
    if session_manager.create_session(name, message.from_user.id, message.chat.id):
        bot.reply_to(message, 'Session created')
    else:
        bot.reply_to(message, 'Failed to create: there is a session already created by you in this chat.')


@bot.message_handler(commands=['delete'])
@group
@authorize
@logging
def delete_session(message):
    if session_manager.delete_session(message.from_user.id, message.chat.id):
        bot.reply_to(message, 'Session deleted')
    else:
        bot.reply_to(message, 'Failed to delete: there are no sessions created by you in this chat.')


@bot.message_handler(commands=['name'])
@group
@authorize
@logging
def rename_session(message):
    new_name = ' '.join(message.text.split(maxsplit=1)[1:]).strip()
    name = session_manager.rename(message.from_user.id, message.chat.id, new_name)
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
    desc = session_manager.description(message.from_user.id, message.chat.id, new_desc)
    if desc:
        bot.reply_to(message, 'Session description: '+desc)
    elif new_desc and not desc:
        bot.reply_to(message, 'Failed to change description: there is no session created by you in this chat.')
    else:
        bot.reply_to(message, 'There is nothing to show')


@bot.message_handler(commands=['start', 'embark'])
@authorize
@group
@logging
def start_session(message):
    session = session_manager.active_chat_session(message.chat.id)
    if not session or session.status:
        return
    if session.id not in session_manager.get_player_sessions(message.from_user.id):
        return

    if session_manager.start(session.id):
        bot.reply_to(message, 'Strike the earth!')
    else:
        bot.reply_to(message, 'You are not prepared for a journey!')


@bot.message_handler(commands=['stop', 'abandon'])
@authorize
@group
@logging
def stop_session(message):
    session = session_manager.active_chat_session(message.chat.id)
    if not session:
        return
    if session.id not in session_manager.get_player_sessions(message.from_user.id):
        return

    if session_manager.stop(session.id):
        bot.reply_to(message, 'Session was stopped')
    else:
        bot.reply_to(message, 'There is nothing to stop')
