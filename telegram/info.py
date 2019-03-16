from telegram import bot
from telegram.decorators import *
from db.manager import user_session_manager, session_manager, user_manager


def get_session(arg):
    session = session_manager.by_name(arg) or session_manager.get(arg)
    return session or None


def info_message(session):
    players, cur = user_session_manager.get_players(session)
    if players:
        players = '\n'.join(f'{k}: {v.get_name()}' for k, v in players.items())
        players = f'Players list:\n{players}'
        if cur:
            players += f'\nCurrent player: {cur.user.get_name()}\nCurrent step: {cur.position}'

    text = f'Session ID #{session.id}\n'
    text += f'Session name: {session.name}\n'

    if session.description:
        text += f'Session description: {session.description}\n'
    if session.folder:
        text += f'Google folder: https://drive.google.com/drive/folders/{session.folder}\n'
    if session.document:
        text += f'Google doc: https://docs.google.com/document/d/{session.document}\n'
    if session.album:
        text += f'ImGur album: https://imgur.com/a/{session.album}\n\n'
    if players:
        text += players

    return text


@bot.message_handler(commands=['info'])
@group
@logging
def info(message):
    arg = ' '.join(message.text.split(maxsplit=1)[1:]).strip()
    session = get_session(arg) if arg else session_manager.active_chat_session(message.chat.id)

    if not session:
        bot.reply_to(message, 'There is nothing to show')
    else:
        bot.reply_to(message, info_message(session))


@bot.message_handler(commands=['my'])
@authorize
@private
@logging
def player_info(message):
    from_user = user_manager.get(message.from_user.id)
    curator_session_query = session_manager.by_curator(from_user)
    active_session_query = session_manager.by_curator(from_user, activeOnly=True)
    player_game_query = user_session_manager.by_player(from_user)
    active_game_query = user_session_manager.by_player(from_user, activeOnly=True)
    text = ''

    if curator_session_query:
        curator = '\n'.join([f'{session}: {session.name}' for session in curator_session_query])
        text += f'\n\nYour as curator in session(s) [id: name]:\n{curator}'
    if active_session_query:
        active_curator = '\n'.join([f'{session}: {session.name}' for session in active_session_query])
        text += f'\n\nYour as curator in active session(s) [id: name]:\n{active_curator}'.format()
    if player_game_query:
        player = '\n'.join([f'{session}: {session.name}' for session in player_game_query])
        text += f'\n\nSessions in which you participate [id: name]:\n{player}'
    if active_game_query:
        active_player = '\n'.join([f'{session}: {session.name}' for session in active_game_query])
        text += f'\n\nYour active games [id: name]:\n{active_player}'

    if not text:
        bot.reply_to(message, 'There is nothing to show')
    else:
        text = f'Total info: {text}'
        bot.reply_to(message, text)


@bot.message_handler(commands=['players'])
@group
@logging
def show_players(message):
    session = session_manager.active_chat_session(message.chat.id)
    players, cur = user_session_manager.get_players(session)
    reply_text = '\n'.join(f'{k}: {v.get_name()}' for k, v in players.items())
    reply_text = f'Players list:\n{reply_text}'
    if cur:
        reply_text += f'\nCurrent player: {cur.user.get_name()}\nCurrent step: {cur.position}'
    if players:
        bot.reply_to(message, reply_text)
    else:
        bot.reply_to(message, 'There are no players')
