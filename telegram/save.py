import requests
from telebot import types

from db.manager import SaveManager, UserSessionManager

from telegram import bot
from telegram.decorators import *
from config.telegram import token as api_token

hideBoard = types.ReplyKeyboardRemove()
chosen_sessions = {}


@bot.message_handler(commands=['retire'])
@authorise
@private
@logging
def close_step(message):
    sessions = UserSessionManager.get_active_sessions(message.from_user.id)
    if not sessions:
        return None
    reply_text = '\n'.join([str(k) + ': ' + v for k, v in sessions.items()])
    reply_text = 'Please chose one\n' + reply_text
    session_select = types.ReplyKeyboardMarkup(one_time_keyboard=True, row_width=len(sessions))
    session_select.add(*[str(k) for k in sessions.keys()])
    session_select.add('Cancel')
    msg = bot.reply_to(message, reply_text, reply_markup=session_select)
    bot.register_next_step_handler(msg, process_session_choose)


def process_session_choose(message):
    if message.text == 'Cancel':
        bot.reply_to(message, 'Okay.jpg', reply_markup=hideBoard)
        return

    user_session = UserSessionManager.get_by_id(message.text)
    chosen_sessions[message.from_user.id] = user_session
    msg = bot.reply_to(message, 'Send a save', reply_markup=hideBoard)
    bot.register_next_step_handler(msg, process_get_file)


def process_get_file(message):
    user_session = chosen_sessions.pop(message.from_user.id)
    file_info = bot.get_file(message.document.file_id)
    file = requests.get('https://api.telegram.org/file/bot{0}/{1}'.format(api_token, file_info.file_path))
    SaveManager.write_save(file.content, user_session)
    UserSessionManager.step(user_session)
    bot.reply_to(message, 'Your turn came to an end!')
