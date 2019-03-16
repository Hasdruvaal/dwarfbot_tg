from aiohttp import web

from utils.logger import init_logging
from logging import info

from db.create_db import init_db

import config
import telegram


if __name__ == '__main__':
    init_logging()
    init_db()
    info('Starting the bot')
    telegram.bot.remove_webhook()
    if config.dev_mode:
        telegram.bot.polling()
    else:
        import webhook
        telegram.bot.set_webhook(url=config.webhook_url_base + config.webhook_url_path,
                                 certificate=open(config.webhook_ssl_cert, 'r'))

        info('Starting the webhook')
        web.run_app(webhook.hook,
                    host=config.webhook_listen,
                    port=config.webhook_port,
                    ssl_context=webhook.ssl_context,
                    )
