#!/usr/bin/env python

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, InlineQueryHandler
from telegram import InlineQueryResultArticle, ParseMode, InputTextMessageContent
from telegram.utils.helpers import escape_markdown
import logging
import json
import datetime
import dvs
import bot_handlers
from uuid import uuid4


# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

def main():
    """Start the bot."""

    config = json.load(open('conf/config.json'))

    # Create the EventHandler and pass it your bot's token.
    updater = Updater(config['token'])

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", bot_handlers.start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("trein", bot_handlers.trein, pass_args=True))

    dp.add_handler(InlineQueryHandler(bot_handlers.inlinequery))

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()