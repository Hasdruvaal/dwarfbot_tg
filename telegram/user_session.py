from config import tg_token
from telegram import bot
from telegram.decorators import *
from db.manager import userSessionManager, sessionManager, userManager
from telegram.info import show_players

from cloud import googleDocs
import images


@bot.message_handler(commands=['toggle'])
@group
@logging
@authorise
def toggle_player(message):
    if message.from_user.is_bot:
        return
    session = sessionManager.active_chat_session(message.chat.id)
    userManager.add_user(id=message.from_user.id,
                         username=message.from_user.username,
                         first_name=message.from_user.first_name,
                         last_name=message.from_user.last_name)
    if session and session.status is None:
        if userSessionManager.toggle_player(session, message.from_user.id):
            bot.reply_to(message, 'You were added to the session game')
        else:
            bot.reply_to(message, 'You were deleted from the session game')
    else:
        bot.reply_to(message, 'Failed to toggle you to the game: there is no game session.')


@bot.message_handler(commands=['shuffle'])
@group
@logging
@authorise
def shuffle_players(message):
    session = sessionManager.active_chat_session(message.chat.id)
    if not session:
        return
    if session.id not in sessionManager.get_player_sessions(message.from_user.id):
        return

    if userSessionManager.shuffle_players(session):
        show_players(message)
    else:
        bot.reply_to(message, 'Failed to shuffle: there is no one to shuffle')


@bot.message_handler(commands=['skip'])
@group
@authorise
@logging
def skip_player(message):
    session = sessionManager.active_chat_session(message.chat.id)
    if not session or session.id not in sessionManager.get_player_sessions(message.from_user.id):
        return

    old, new = userSessionManager.step(session)
    if old:
        bot.send_message(old.user, 'Sorry! Your step was skipped!')
        bot.send_message(session.chat, 'Current player is skipped!')
    if new:
        save_id = userSessionManager.write_from_prev(old)
        if save_id:
            bot.send_message(new.user, 'Your turn!\nDownload the save: ' + googleDocs.get_link(save_id))
        else:
            bot.send_message(new.user, 'Your turn!\nYou are the first!')
    else:
        bot.send_message(session.chat, 'The round of game is end.')


@bot.message_handler(commands=['add'])
@group
@authorise
@logging
def add_player(message):
    session = sessionManager.active_chat_session(message.chat.id)
    if not session:
        return

    if session.id in sessionManager.get_player_sessions(message.from_user.id):
        if message.reply_to_message:
            reply = message.reply_to_message
            if reply.from_user.is_bot:
                return
            to_add = userManager.get(reply.from_user.id)
            if not to_add:
                bot.reply_to(message, 'Player must do /auth before adding!')
                return
            if userSessionManager.toggle_player(user_id=to_add,
                                                session_id=session,
                                                force_add=True):
                bot.reply_to(message, 'Player was added!')
            else:
                bot.reply_to(message, 'Something went wrong')
        else:
            bot.reply_to(message, 'You must reply to the id message for add that id!')


@bot.message_handler(commands=['round'])
@authorise
@group
@logging
def close_round(message):
    shuffle = ' '.join(message.text.split(maxsplit=1)[1:]).strip() or None
    session = sessionManager.active_chat_session(message.chat.id)
    if not session:
        return
    if session.id not in sessionManager.get_player_sessions(message.from_user.id):
        return

    if userSessionManager.round(session.id, shuffle):
        bot.reply_to(message, 'Round was added')
    else:
        bot.reply_to(message, 'Cant make round')


@bot.message_handler(commands=['fact'])
@bot.message_handler(func=lambda x: x.caption and '/fact' in x.caption, content_types=['photo'])
@authorise
@group
def fact(message):
    session = sessionManager.active_chat_session(message.chat.id)
    if not session:
        return

    text, img = None, None
    if message.content_type == 'text':
        text = ' '.join(message.text.split(maxsplit=1)[1:]).strip() or ''
    elif message.caption and '/fact' in message.caption:
        text = message.caption.replace('/fact ', '') or ''

        file_info = bot.get_file(message.photo[len(message.photo)-1].file_id)
        img = images.client.upload_from_url('https://api.telegram.org/file/bot{0}/{1}'.format(tg_token,
                                                                                              file_info.file_path),
                                            config={'album': session.album},
                                            anon=False).get('link')
    else:
        return

    current_session = userSessionManager.get_players(session)[-1]
    sender = userManager.get(message.from_user.id)

    if sender == current_session.user and (text or img):
        googleDocs.add_data(document_id=session.document,
                            owner=sender.get_name(),
                            text=text.strip(),
                            image=img)
        bot.reply_to(message, session.hashtag())
