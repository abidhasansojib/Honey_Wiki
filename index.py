import logging
from telegram.ext import Updater, CommandHandler
import wikipedia

# Set up logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

# Function to handle the /start command
def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Hello! I'm a Wikipedia bot. Send me a query and I'll fetch information for you.")

# Function to handle queries
def search(update, context):
    query = " ".join(context.args)
    try:
        summary = wikipedia.summary(query)
        context.bot.send_message(chat_id=update.effective_chat.id, text=summary)
    except wikipedia.exceptions.PageError:
        context.bot.send_message(chat_id=update.effective_chat.id, text="No information found for that query.")
    except wikipedia.exceptions.DisambiguationError as e:
        options = "\n".join(e.options)
        context.bot.send_message(chat_id=update.effective_chat.id, text=f"Multiple options found. Please be more specific:\n{options}")

def main():
    # Create an instance of the Updater class
    updater = Updater(token='YOUR_TELEGRAM_BOT_TOKEN', use_context=True)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # Register the handlers for commands
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("search", search))

    # Start the bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C
    updater.idle()

if __name__ == '__main__':
    main()