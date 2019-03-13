from aiohttp import web
import time

from utils.logger import init_logging
from logging import info

from db.create_db import init_db

import config
import telegram
import webhook


if __name__ == '__main__':
    init_logging()
    #init_db()

    info('Starting the bot')
    telegram.bot.remove_webhook()
    time.sleep(0.25)
    telegram.bot.set_webhook(url=config.webhook_url_base + config.webhook_url_path,
                             certificate=open(config.webhook_ssl_cert, 'r'))

    info('Starting the webhook')
    web.run_app(webhook.hook,
                host=config.webhook_listen,
                port=config.webhook_port,
                ssl_context=webhook.ssl_context,
                )
