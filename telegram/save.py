import requests
import os
from telebot import types
from logging import error

from db.manager import userSessionManager

from telegram import bot
from telegram.decorators import *
from config import tg_token, tg_proxy

from cloud import googleDrive


@bot.message_handler(commands=['retire','save'])
@authorise
@private
@logging
def close_step(message):
    sessions = userSessionManager.all_player_active(message.from_user.id)
    if sessions:
        reply_text = '\n'.join([f'{k}: {v}' for k, v in sessions.items()])
        reply_text = 'Please chose one\n' + reply_text
        session_select = types.ReplyKeyboardMarkup(one_time_keyboard=True, row_width=len(sessions))
        session_select.add(*[str(k) for k in sessions.keys()])
        session_select.add('Cancel')
        msg = bot.reply_to(message, reply_text, reply_markup=session_select)
        bot.register_next_step_handler(msg, process_session_choose)
    else:
        bot.reply_to(message, 'No active sessions')


def process_session_choose(message):
    if message.text == 'Cancel':
        bot.reply_to(message, 'Okay.jpg', reply_markup=types.ReplyKeyboardRemove())
        return

    user_session = userSessionManager.get(message.text)
    msg = bot.reply_to(message, 'Send a save', reply_markup=types.ReplyKeyboardRemove())
    bot.register_next_step_handler(msg, process_get_file, user_session)


def process_get_file(message, chosen_session):
    user_session = userSessionManager.get(chosen_session)
    file_info = bot.get_file(message.document.file_id)
    try:
        file = requests.get(f'https://api.telegram.org/file/bot{tg_token}/{file_info.file_path}', proxies=tg_proxy)
        if file.status_code != 200:
            raise Exception('Cant download save-game')
    except Exception as e:
        error(e)
        bot.reply_to(message, 'Something went wrong!')
        return

    file_name = user_session.game_name()
    with open(file_name, 'wb') as f:
        f.write(file.content)
    save_id = googleDrive.upload_file(file_name, file_name, user_session.session.folder)
    os.remove(file_name)

    userSessionManager.write_save(save_id, user_session)

    old, new = userSessionManager.step(user_session.session)
    bot.reply_to(message, 'Your turn came to the end!')
    if new:
        bot.send_message(new.user, f'Your turn!\nDownload the save: {googleDrive.get_link(save_id)}')
    else:
        bot.send_message(old.session.chat, f'The round of game is end. Last save: {googleDrive.get_link(save_id)}')
