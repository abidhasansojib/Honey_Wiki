import os
from io import BytesIO
from queue import Queue
import requests
from flask import Flask, request
from telegram import Bot, Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CommandHandler, MessageHandler, Filters, CallbackQueryHandler, Dispatcher
from wikipedia import Wikipedia

TOKEN = os.getenv("TOKEN")
URL = os.getenv("URL")
bot = Bot(TOKEN)
wiki = Wikipedia()

def welcome(update, context) -> None:
    update.message.reply_text(f"Hello {update.message.from_user.first_name}, Welcome to SB Movies.\n"
                              f"🚀 Explore the world of movies with Wikipedia.")
    update.message.reply_text("👇 Enter Movie Name 👇")


def search_movie(update, context):
    search_results = update.message.reply_text("Processing...")
    query = update.message.text
    try:
        wiki_summary = wiki.summary(query, sentences=2)
        reply_text = f"🎬 {query}\n\n{wiki_summary}"
        update.message.edit_text(reply_text)
    except:
        update.message.edit_text(f"Sorry, I couldn't find any information about {query} on Wikipedia.")


def setup():
    update_queue = Queue()
    dispatcher = Dispatcher(bot, update_queue, use_context=True)
    dispatcher.add_handler(CommandHandler('start', welcome))
    dispatcher.add_handler(MessageHandler(Filters.text, search_movie))
    return dispatcher


app = Flask(__name__)


@app.route('/')
def index():
    return 'Hello World!'


@app.route('/{}'.format(TOKEN), methods=['GET', 'POST'])
def respond():
    update = Update.de_json(request.get_json(force=True), bot)
    setup().process_update(update)
    return 'ok'


@app.route('/setwebhook', methods=['GET', 'POST'])
def set_webhook():
    s = bot.setWebhook('{URL}/{HOOK}'.format(URL=URL, HOOK=TOKEN))
    if s:
        return "webhook setup ok"
    else:
        return "webhook setup failed"
