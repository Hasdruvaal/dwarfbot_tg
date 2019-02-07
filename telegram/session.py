from telebot import types

from telegram import bot
from telegram.decorators import *
from db.models import SessionManager, User, Session

hideBoard = types.ReplyKeyboardRemove()
chosen_sessions = {}


@bot.message_handler(commands=['create_session'])
@group
@authorise
@logging
def create_session(message):
    name = ' '.join(message.text.split(maxsplit=1)[1:]) or 'Untitled'
    ok = SessionManager.createSession(name, message.from_user.id, message.chat.id)
    if ok:
        bot.reply_to(message, "Session is created")
    else:
        bot.reply_to(message, "Failed to create: there is one already created by you in this chat.")


@bot.message_handler(commands=['delete_session'])
@private
@authorise
@logging
def delete_session(message):
    user = User.get_by_id(message.from_user.id)
    sessions = Session.filter(curator=user)
    session_mapping = {s.sessionId: s.name for s in sessions}

    reply_text = '\n'.join(str(k) + ': ' + v for k, v in session_mapping.items())
    reply_text = 'Please chose one\n' + reply_text
    session_select = types.ReplyKeyboardMarkup(one_time_keyboard=True, row_width=len(sessions))
    session_select.add(*[str(k) for k in session_mapping.keys()])
    session_select.add('Cancel')
    msg = bot.reply_to(message, reply_text, reply_markup=session_select)
    bot.register_next_step_handler(msg, process_deletion_choose)


def process_deletion_choose(message):
    if message.text == 'Cancel':
        bot.reply_to(message, 'Okay.jpg', reply_markup=hideBoard)
        return

    try:
        Session.delete_by_id(message.text)
        bot.reply_to(message, 'Successfully deleted.', reply_markup=hideBoard)
    except Exception:
        bot.reply_to(message, 'Something gone wrong!', reply_markup=hideBoard)


@bot.message_handler(commands=['rename_session'])
@authorise
@private
@logging
def rename_session(message):
    user = User.get_by_id(message.from_user.id)
    sessions = Session.filter(curator=user)
    session_mapping = {s.sessionId: s.name for s in sessions}

    reply_text = '\n'.join([str(k) + ': ' + v for k, v in session_mapping.items()])
    reply_text = 'Please chose one\n' + reply_text
    session_select = types.ReplyKeyboardMarkup(one_time_keyboard=True, row_width=len(sessions))
    session_select.add(*[str(k) for k in session_mapping.keys()])
    session_select.add('Cancel')
    msg = bot.reply_to(message, reply_text, reply_markup=session_select)
    bot.register_next_step_handler(msg, process_session_choose)


def process_session_choose(message):
    if message.text == 'Cancel':
        bot.reply_to(message, 'Okay.jpg', reply_markup=hideBoard)
        return
    session = Session.get_by_id(message.text)
    chosen_sessions[message.from_user.id] = session

    msg = bot.reply_to(message, 'Define a new name', reply_markup=hideBoard)
    bot.register_next_step_handler(msg, process_name_typing)


def process_name_typing(m):
    name = m.text
    session: Session = chosen_sessions.get(m.from_user.id)
    if session:
        session.name = name
        session.save()
        bot.reply_to(m, 'Success')
    else:
        bot.reply_to(m, 'Couldn\'t find any sessions!')


@bot.message_handler(commands=['set_description'])
@private
@authorise
@logging
def set_description(message):
    user = User.get_by_id(message.from_user.id)
    sessions = Session.filter(curator=user)
    session_mapping = {s.sessionId: s.name for s in sessions}

    reply_text = '\n'.join(str(k) + ': ' + v for k, v in session_mapping.items())
    reply_text = 'Please chose one\n' + reply_text
    session_select = types.ReplyKeyboardMarkup(one_time_keyboard=True, row_width=len(sessions))
    session_select.add(*[str(k) for k in session_mapping.keys()])
    session_select.add('Cancel')
    msg = bot.reply_to(message, reply_text, reply_markup=session_select)
    bot.register_next_step_handler(msg, process_description_choose)


def process_description_choose(message):
    if message.text == 'Cancel':
        bot.reply_to(message, 'Okay.jpg', reply_markup=hideBoard)
        return
    session = Session.get_by_id(message.text)
    chosen_sessions[message.from_user.id] = session

    msg = bot.reply_to(message, 'Define a description', reply_markup=hideBoard)
    bot.register_next_step_handler(msg, process_name_typing)


def process_description_typing(m):
    description = m.text
    session: Session = chosen_sessions.get(m.from_user.id)
    if session:
        session.name = description
        session.save()
        bot.reply_to(m, 'Success')
    else:
        bot.reply_to(m, 'Couldn\'t find any sessions!')

