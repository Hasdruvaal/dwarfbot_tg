from telebot import types
from aiohttp import web
from telegram import bot

import config
import ssl


hook = web.Application()


async def handle(request):
    if request.match_info.get('token') == bot.token:
        request_body_dict = await request.json()
        update = types.Update.de_json(request_body_dict)
        bot.process_new_updates([update])
        return web.Response()
    else:
        return web.Response(status=403)


hook.router.add_post('/%s/' % (config.tg_token), handle)
ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
ssl_context.load_cert_chain(config.webhook_ssl_cert, config.webhook_ssl_priv)
