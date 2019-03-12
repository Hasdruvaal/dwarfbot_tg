from utils.logger import init_logging
from logging import info
import time

from db.create_db import init_db

import config
import telegram
import webhook


if __name__ == '__main__':
    init_logging()
    init_db()

    info('Starting the bot')
    telegram.bot.remove_webhook()
    time.sleep(0.25)
    telegram.bot.set_webhook(url=config.webhook_url_base + config.webhook_url_path,
                              certificate=open(config.webhook_ssl_cert, 'r'))

    info('Starting the webhook')
    http_server = tornado.httpserver.HTTPServer(webhook.application, ssl_options={'certfile': config.webhook_cert,
                                                                                  'keyfile' : config.webhook_pkey})
    webhook.tornado.ioloop.PeriodicCallback(webhook.try_exit, 100).start()
    webhook.tornado.ioloop.IOLoop.instance().start()
