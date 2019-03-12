import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web

from telebot import types

import config
from telegram import bot
from logging import info


class webhook_serv(tornado.web.RequestHandler):
    def get(self):
        self.write("What are you doing here?")
        self.finish()

    def post(self):
        if 'Content-Length' in self.request.headers and \
            'Content-Type' in self.request.headers and \
            self.request.headers['Content-Type'] == 'application/json':

            json_data = self.request.body.decode("utf-8")
            update = types.Update.de_json(json_data)
            bot.process_new_updates([update])
            self.write('')
            self.finish()
        else:
            self.write('GTFO')
            self.finish()

tornado.options.define('port', default=config.webhook_port, help='run on the given port', type=int)
is_closing = False

def signal_handler(signum, frame):
    global is_closing
    info('Tornado exiting...')
    is_closing = True

def try_exit():
    global is_closing
    if is_closing:
        tornado.ioloop.IOLoop.instance().stop()
        info('Tornado exit success!')

tornado.options.options.logging = None
tornado.options.parse_command_line()
signal.signal(signal.SIGINT, signal_handler)

application = tornado.web.Application([
    (r'/' + config.webhook_secret, webhook_serv)
])
