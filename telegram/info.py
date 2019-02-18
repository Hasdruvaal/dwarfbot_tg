from telegram import bot
from telegram.decorators import *
from db.manager import userSessionManager, sessionManager, userManager


def get_session(arg):
    ret = sessionManager.by_name(arg) or sessionManager.get(arg)
    return ret or None


def info_message(session):
    players, cur = userSessionManager.get_players(session)
    if players:
        players = '\n'.join(str(k) + ': ' + v.get_name() for k, v in players.items())
        players = 'Players list:\n' + players
        if cur:
            players += '\nCurrent player: @'+cur.user.get_name() + \
                          '\nCurrent step: '+str(cur.position)

    text = 'Session ID #{}\n'.format(session.id)
    text += 'Session name: {}\n'.format(session.name)

    if session.description:
        text += 'Session description: {}\n'.format(session.description or 'No description')
    if session.folder:
        text += 'Google folder: https://drive.google.com/drive/folders/{}\n'.format(session.folder)
    if session.document:
        text += 'Google doc: https://docs.google.com/document/d/{}\n'.format(session.document or 'No doc')
    if session.album:
        text += 'ImGur album: https://imgur.com/a/{}\n\n'.format(session.album or 'No album')
    if players:
        text += players

    return text


@bot.message_handler(commands=['info'])
@group
@logging
def info(message):
    arg = ' '.join(message.text.split(maxsplit=1)[1:]).strip()
    session = get_session(arg) if arg else sessionManager.active_chat_session(message.chat.id)

    if not session:
        bot.reply_to(message, 'There is nothing to show')
    else:
        bot.reply_to(message, info_message(session))


@bot.message_handler(commands=['my'])
@authorise
@private
@logging
def player_info(message):
    from_user = userManager.get(message.from_user.id)
    curator_session_query = sessionManager.by_curator(from_user)
    active_session_query = sessionManager.by_curator(from_user, activeOnly=True)
    player_game_query = userSessionManager.by_player(from_user)
    active_game_query = userSessionManager.by_player(from_user, activeOnly=True)
    text = ''

    if curator_session_query:
        curator = '\n'.join([str(session)+': '+session.name for session in curator_session_query])
        text += '\n\nYour as curator in session(s) [id: name]:\n{}'.format(curator)
    if active_session_query:
        active_curator = '\n'.join([str(session)+': '+session.name for session in active_session_query])
        text += '\n\nYour as curator in active session(s) [id: name]:\n{}'.format(active_curator)
    if player_game_query:
        player = '\n'.join([str(session.session.id)+': '+session.session.name for session in player_game_query])
        text += '\n\nSessions in which you participate [id: name]:\n{}'.format(player)
    if active_game_query:
        active_player = '\n'.join([str(session.session.id)+': '+session.session.name for session in active_game_query])
        text += '\n\nYour active games [id: name]:\n{}'.format(active_player)

    if not text:
        bot.reply_to(message, 'There is nothing to show')
    else:
        text = 'Total info:'+text
        bot.reply_to(message, text)


@bot.message_handler(commands=['players'])
@group
@logging
def show_players(message):
    session = sessionManager.active_chat_session(message.chat.id)
    players, cur = userSessionManager.get_players(session)
    reply_text = '\n'.join(str(k) + ': ' + v.get_name() for k, v in players.items())
    reply_text = 'Players list:\n' + reply_text
    if cur:
        reply_text += '\nCurrent player: @'+cur.user.get_name() + \
                      '\nCurrent step: '+str(cur.position)
    if players:
        bot.reply_to(message, reply_text)
    else:
        bot.reply_to(message, 'There are no players')
