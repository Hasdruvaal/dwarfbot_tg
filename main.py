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


chosen_sessions = {}


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


print("Starting the bot")
bot.polling()
