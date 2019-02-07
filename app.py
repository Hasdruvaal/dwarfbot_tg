from utils import logger
from logging import info

import telegram

if __name__ == '__main__':
    info("Starting the bot")
    telegram.bot.polling()
