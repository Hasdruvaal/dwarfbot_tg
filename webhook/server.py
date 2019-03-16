from telebot import types
from aiohttp import web
from telegram import bot

import config
import ssl


async def handle(request):
    if request.body_exists:
        request_body_dict = await request.json()
        update = types.Update.de_json(request_body_dict)
        bot.process_new_updates([update])
        return web.Response()
    else:
        return web.Response(status=403)

hook = web.Application()
hook.router.add_post(f'/{config.tg_token}/', handle)
ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
ssl_context.load_cert_chain(config.webhook_ssl_cert, config.webhook_ssl_priv)
