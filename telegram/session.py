from telegram import bot
from telegram.decorators import *
from db.manager import SessionManager


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
    new_name = ' '.join(message.text.split(maxsplit=1)[1:]).strip()
    name = SessionManager.rename_session(message.from_user.id, message.chat.id, new_name)
    if name and not new_name:
        bot.reply_to(message, 'Session name: '+name)
    elif name and new_name:
        bot.reply_to(message, 'Session name changed!')
    elif new_name and not name:
        bot.reply_to(message, 'Failed to change name: there is no session created by you in this chat.')
    else:
        bot.reply_to(message, 'There is nothing to show')


@bot.message_handler(commands=['description'])
@private
@logging
def description(message):
    new_desc = ' '.join(message.text.split(maxsplit=1)[1:]).strip() or None
    desc = SessionManager.description(message.from_user.id, message.chat.id, new_desc)
    if desc and not new_desc:
        bot.reply_to(message, 'Session description: '+desc)
    elif desc and new_desc:
        bot.reply_to(message, 'Session description changed!')
    elif new_desc and not desc:
        bot.reply_to(message, 'Failed to change description: there is no session created by you in this chat.')
    else:
        bot.reply_to(message, 'There is nothing to show')


@bot.message_handler(commands=['embark'])
@authorise
@private
@logging
def start_session(message):
    session_id = SessionManager.get_chat_session(message.chat.id).sessionId
    if not session_id:
        return
    if session_id not in SessionManager.get_player_sessions(message.from_user.id):
        return

    if SessionManager.start_session(session_id):
        bot.reply_to(message, 'Strike the earth!')
    else:
        bot.reply_to(message, 'You are not prepared to journey!')
