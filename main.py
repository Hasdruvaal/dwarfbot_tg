import telebot
import log

import config
telebot.apihelper.proxy = {'https':config.proxy}
bot = telebot.TeleBot(config.token)
print("Ok")

@bot.message_handler(commands=['start', 'help'])
def send_greeting(message):
	log.logi(message, "Greeting sent")
	bot.send_message(message.chat.id, "Greetings! Make in progress")

bot.polling()