import os

from telegram import bot
from telegram.decorators import *
from db.manager import UserSessionManager, SessionManager, UserManager

from cloud import googleDocs


@bot.message_handler(commands=['toggle'])
@group
@logging
def toggle_player(message):
    session = SessionManager.get_chat_session(message.chat.id)
    UserManager.add_user(message.from_user.id,
                         message.chat.id,
                         message.from_user.username,
                         message.from_user.first_name,
                         message.from_user.last_name)
    if session and session.status is None:
        if UserSessionManager.toggle_player(session, message.from_user.id):
            bot.reply_to(message, 'You were added to the session game')
        else:
            bot.reply_to(message, 'You were deleted from the session game')
    else:
        bot.reply_to(message, 'Failed to toggle you to the game: there is no game session.')


@bot.message_handler(commands=['players'])
@group
@logging
def players(message):
    session = SessionManager.get_chat_session(message.chat.id)
    players, cur = UserSessionManager.get_players(session)
    reply_text = '\n'.join(str(k) + ': ' + v.get_name() for k, v in players.items())
    reply_text = 'Players list:\n' + reply_text
    if cur:
        reply_text += '\nCurrent player: @'+cur.user.get_name() + \
                      '\nCurrent step: '+str(cur.position)
    if players:
        bot.reply_to(message, reply_text)
    else:
        bot.reply_to(message, 'There are no players')


@bot.message_handler(commands=['shuffle'])
@group
@logging
def shuffle_player(message):
    session = SessionManager.get_chat_session(message.chat.id)
    if not session:
        return
    if session.id not in SessionManager.get_player_sessions(message.from_user.id):
        return

    if session and UserSessionManager.shuffle_players(message.chat.id, session):
        players(message)
    else:
        bot.reply_to(message, 'Failed to shuffle: there is no one to shuffle')


@bot.message_handler(commands=['skip'])
@group
@authorise
@logging
def skip_player(message, text=None):
    session = SessionManager.get_chat_session(message.chat.id)
    if not session:
        return
    if session.id in SessionManager.get_player_sessions(message.from_user.id):
        old, new = UserSessionManager.step(session)
        if new:
            bot.reply_to(message, 'Current player is skipped!')
            bot.send_message(old.user, 'Sorry! But your step was skipped by curator' if not text else text)
            save_id = UserSessionManager.write_perv(old)
            if save_id:
                bot.send_message(new.user, 'Your turn!\nDownload the save: ' + googleDocs.get_link(save_id))


@bot.message_handler(commands=['add'])
@group
@authorise
@logging
def add_player(message):
    session = SessionManager.get_chat_session(message.chat.id)
    if not session:
        return

    if session.id in SessionManager.get_player_sessions(message.from_user.id):
        if message.reply_to_message:
            if not UserManager.check_user(message.reply_to_message.from_user.id):
                bot.reply_to(message, 'Player must auth!')
                return
            if UserSessionManager.toggle_player(user_id=message.reply_to_message.from_user.id,
                                                session_id=session,
                                                force_add=True):
                bot.reply_to(message, 'Player was added!')
            else:
                bot.reply_to(message, 'Something went wrong')
        else:
            bot.reply_to(message, 'You must reply to the user message for add that user!')


@bot.message_handler(commands=['round'])
@authorise
@group
@logging
def round(message):
    shuffle = ' '.join(message.text.split(maxsplit=1)[1:]).strip() or None
    session = SessionManager.get_chat_session(message.chat.id)
    if not session:
        return
    if session.id not in SessionManager.get_player_sessions(message.from_user.id):
        return

    if UserSessionManager.round(session.id, shuffle):
        bot.reply_to(message, 'Round was added')
    else:
        bot.reply_to(message, 'Cant make round')


@bot.message_handler(commands=['fact'])
@bot.message_handler(content_types=['photo'])
@authorise
@group
def fact(message):
    session = SessionManager.get_chat_session(message.chat.id)
    if not session:
        return

    text, img = None, None
    if message.content_type == 'text':
        text = message.text
    elif message.caption and '/fact' in message.caption:
         text = message.caption.replace('/fact ', '')
         img = 'https://github.com/dtsvetkov1/Google-Drive-sync/raw/master/google-drive-logo-logo.png'
         # TODO: download and add photo to imgur, add image-url here
    else:
        return

    text = ' '.join(text.split(maxsplit=1)[1:]).strip() or None

    current_session = UserSessionManager.get_players(session)[-1]
    sender = UserManager.get_user(message.from_user.id)

    if sender == current_session.user:
        googleDocs.add_data(
                document_id=current_session.session.cloud_doc,
                owner=sender.get_name(),
                text=text,
                image=img
            )
        bot.reply_to(message, current_session.session.hashtag())
