from telegram import bot
from telegram.decorators import *
from db.manager import UserSessionManager, SessionManager, UserManager


@bot.message_handler(commands=['toggle'])
@private  # TODO: change to group - private is for test only
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
@private  # TODO: change to group - private is for test only
@logging
def players(message):
    session = SessionManager.get_chat_session(message.chat.id)
    players = UserSessionManager.get_players(session)
    reply_text = '\n'.join(str(k) + ': ' + v for k, v in players.items())
    reply_text = 'Players list:\n' + reply_text
    if players:
        bot.reply_to(message, reply_text)
    else:
        bot.reply_to(message, 'There are no players')


@bot.message_handler(commands=['shuffle'])
@private  # TODO: change to group - private is for test only
@logging
def shuffle_player(message):
    session = SessionManager.get_chat_session(message.chat.id)
    if session and UserSessionManager.shuffle_players(message.chat.id, session):
        players(message)
    else:
        bot.reply_to(message, 'Failed to shuffle: there is no one to shuffle')


@bot.message_handler(commands=['skip'])
@private  # TODO: change to group - private is for test only
@authorise
@logging
def skip_player(message):
    session = SessionManager.get_chat_session(message.chat.id)
    if not session:
        return
    if session.sessionId in SessionManager.get_player_sessions(message.chat.id):
        if UserSessionManager.step(session):
            bot.reply_to(message, 'Current player is skipped!')


@bot.message_handler(commands=['round'])
@private  # TODO: change to group - private is for test only
@authorise
@logging
def close_round(message):
    return # TODO: at last player create change

