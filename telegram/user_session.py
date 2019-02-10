from telegram.decorators import *
from db.manager import UserSessionManager, SessionManager


@bot.message_handler(commands=['toggle'])
@private  # TODO: change to group - private is for test only
@logging
def toggle_player(message):
    session = SessionManager.get_session(message.chat.id)
    if session:
        if UserSessionManager.toggle_player(session, message.from_user.id):
            bot.reply_to(message, 'You was added to session game')
        else:
            bot.reply_to(message, 'You was deleted to session game')
    else:
        bot.reply_to(message, 'Failed to toggle you to game: there is no game session.')


@bot.message_handler(commands=['players'])
@private  # TODO: change to group - private is for test only
@logging
def players(message):
    session = SessionManager.get_session(message.chat.id)
    players = UserSessionManager.get_players(session)
    reply_text = '\n'.join(str(k+1) + ': ' + v for k, v in players.items())
    reply_text = 'Players list:\n' + reply_text
    if players:
        bot.reply_to(message, reply_text)
    else:
        bot.reply_to(message, 'There is no any player')


@bot.message_handler(commands=['shuffle'])
@private  # TODO: change to group - private is for test only
@logging
def shuffle_player(message):
    session = SessionManager.get_session(message.chat.id)
    if UserSessionManager.shuffle_players(message.chat.id, session):
        players(message)
    else:
        bot.reply_to(message, 'Failed to shuffle: there is nothing to shuffle')

