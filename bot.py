#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This program is dedicated to the public domain under the CC0 license.

"""
Simple Bot to reply to Telegram messages.
First, a few handler functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.
Usage:
Basic Echobot example, repeats messages.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""

import logging
import requests
import json
import os

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, Defaults
from telegram import ParseMode

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def duc_meme(update, context):
    update.message.bot.send_photo(chat_id=update.message.chat_id, photo=open('./img/wait.jpg', 'rb'))

def a_meme(update, context):
    js = json.loads(requests.get("https://meme-api.herokuapp.com/gimme").text)
    update.message.bot.send_photo(chat_id=update.message.chat_id, photo=js['url'], reply_to_message_id=update.message.message_id)

def a_gif(update, context):
    s = update.message.text.split(' ')
    keyword = 'not working'
    if len(s) > 1:
        keyword = s[1]
    if keyword == 'conghm1':
        update.message.reply_text("Rejected, animation contains sensitive content.") 
    else:
        js = json.loads(requests.get("https://api.tenor.com/v1/random?key=LIVDSRZULELA&limit=1&q="+keyword).text)
        if not js['results']:
            update.message.reply_text("No gif found, don't wait") 
        else:
            update.message.bot.send_animation(chat_id=update.message.chat_id, animation=js['results'][0]['media'][0]['tinygif']['url'], reply_to_message_id=update.message.message_id)

def quote(update, context):
    js = json.loads(requests.get("https://api.quotable.io/random").text)
    msg = '<code>"' + js['content'] + '"</code>' +  '\n- ' + js['author']
    update.message.reply_text('Quote of the day: \n {}'.format(msg)) 

def joke(update, context):
    js = json.loads(requests.get("https://sv443.net/jokeapi/v2/joke/Any?type=single").text)
    msg = js['joke']
    update.message.reply_text(msg) 

def main():
    defaults = Defaults(parse_mode=ParseMode.HTML)
    updater = Updater(os.getenv('BOT_SECRETKEY'), use_context=True, defaults=defaults)

    dp = updater.dispatcher

    dp.add_handler(CommandHandler("insert_duc_meme", duc_meme))
    dp.add_handler(CommandHandler("insert_a_meme", a_meme))
    dp.add_handler(CommandHandler("insert_a_gif", a_gif))
    dp.add_handler(CommandHandler("joke", joke))
    dp.add_handler(CommandHandler("quote", quote))


    dp.add_error_handler(error)

    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    main()