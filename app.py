from utils.logger import init_logging
from logging import info
from db.create_db import init_db

import telegram


if __name__ == '__main__':
    init_logging()
    init_db()
    info('Starting the bot')
    telegram.bot.polling()

