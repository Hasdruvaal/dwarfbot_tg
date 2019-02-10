from telegram import bot
from telegram.decorators import *
from db.manager import UserSessionManager, SessionManager, UserManager


@bot.message_handler(commands=['toggle'])
@private  # TODO: change to group - private is for test only
@logging
def toggle_player(message):
    session = SessionManager.get_session(message.chat.id)
    UserManager.add_user(message.from_user.id,
                         message.chat.id,
                         message.from_user.username,
                         message.from_user.first_name,
                         message.from_user.last_name
                         )
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
    if session and UserSessionManager.shuffle_players(message.chat.id, session):
        players(message)
    else:
        bot.reply_to(message, 'Failed to shuffle: there is nothing to shuffle')


@bot.message_handler(commands=['skip'])
@private  # TODO: change to group - private is for test only
@authorise
@logging
def skip_player(message):
    return # TODO: delete current player from UserSession, and set active to the next

@bot.message_handler(commands=['round'])
@private  # TODO: change to group - private is for test only
@authorise
@logging
def close_round(message):
    return # TODO: at last player create change

