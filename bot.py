#!/usr/bin/env python

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, InlineQueryHandler
from telegram import InlineQueryResultArticle, ParseMode, InputTextMessageContent
from telegram.utils.helpers import escape_markdown
import logging
import json
import datetime
import dvs
from uuid import uuid4


# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

def treinToText(treininfo):
    if treininfo['via']:
        header = "*{} {} {} richting {} via {}*\n".format(treininfo['vervoerder'], treininfo['soort'], treininfo['treinNr'], treininfo['bestemming'], treininfo['via'])
    else:
        header = "*{} {} {} richting {}*\n".format(treininfo['vervoerder'], treininfo['soort'], treininfo['treinNr'], treininfo['bestemming'])


    if len(treininfo['vleugels']) > 1:
        vleugeltekst = "trein bevat > 1 vleugel, not yet implemented"
    else:
        stops = "*Stops:*\n"
        vleugel = treininfo['vleugels'][0]
        for stop in vleugel['stopstations']:
            if stop['aankomst'] == None and stop['vertrek']: # Beginstation
                stops += "_{}_ ({}) V {} spoor {}\n".format(stop['naam'], stop['code'].upper(), stop['vertrek'], stop['vertrekspoor'])
            elif stop['vertrek'] == None and stop['aankomst']: # Eindstation
                stops += "_{}_ ({}) A {} spoor {}\n".format(stop['naam'], stop['code'].upper(), stop['aankomst'], stop['aankomstspoor'])
            else: # Tussenstation
                stops += "_{}_ ({}) A {} V {} spoor {}\n".format(stop['naam'], stop['code'].upper(), stop['aankomst'], stop['vertrek'], stop['vertrekspoor'])
        stops += "\n"
        
        mat_text = "*Materieel:*\n"
        if len(vleugel['mat']) is 0:
            mat_text += "Materieelinfo niet beschikbaar"
        else:
            for materieel in vleugel['mat']:
                if materieel[2] is None: # geen mat-nr
                    mat_text += "{}, eindbestemming {}\n".format(materieel[0], materieel[1])
                else:
                    mat_text += "{} {}, eindbestemming {}\n".format(materieel[0], materieel[2], materieel[1])

        vleugeltekst = stops + mat_text
            
    notices = ""
    if len(treininfo['tips']) > 0:
        reistips = "*Reistip(s):*\n"
        for tip in treininfo['tips']:
            reistips += tip + "\n"
    else:
        reistips = ""
    if len(treininfo['opmerkingen']) > 0:
        opmerkingen = "*Opmerking(en):*\n"
        for opmerking in treininfo['opmerkingen']:
            opmerkingen += opmerking + "\n"
    else:
        opmerkingen = ""

    if treininfo['opgeheven'] is True:
        opgeheven = "\n\n*Deze trein is opgeheven!*"
    else:
        opgeheven = ""
    
    notices = reistips + opmerkingen + opgeheven
    

    
    return header + vleugeltekst + notices
 


# Define a few command handlers. These usually take the two arguments bot and
# update. Error handlers also receive the raised TelegramError object in error.
def start(bot, update):
    update.message.reply_text('Hello ovdingenbot! /help')

def help(bot, update):
    update.message.reply_text('`/trein <trein_number>` or `/trein <trein_number> <dd-mm-yy>`')

def trein(bot, update, args):
    if len(args) > 2:
        update.message.reply_text("Too many arguments. Try using /help.")
        return False
    if len(args) is 0:
        update.message.reply_text("Too few arguments. Try using /help.")
        return False
    
    treinnummer = args[0]
    if len(args) is 1:
        date = datetime.datetime.today().strftime('%Y-%m-%d')
    else:
        date = args[1]

    train = dvs.train("https://dvs.ovdingen.nl", date, treinnummer)

    message = treinToText(train)
    

    update.message.reply_text(message, parse_mode="Markdown")

def inlinequery(bot, update):
    """Handle the inline query."""
    query = update.inline_query.query

    results = []

    if query.isdigit(): # Query is een getal
        if len(query) < 7: # Treinnummers zijn nooit langer dan 7 cijfers.
            date = datetime.datetime.today().strftime('%Y-%m-%d')
            trein = dvs.train("https://dvs.ovdingen.nl", date, query)
            trein_result = InlineQueryResultArticle(
                id=uuid4(),
                title = "Trein {}".format(query),
                input_message_content=InputTextMessageContent(treinToText(trein), parse_mode="Markdown")
            )
            results.append(trein_result)
    update.inline_query.answer(results)

def main():
    """Start the bot."""

    config = json.load(open('conf/config.json'))

    # Create the EventHandler and pass it your bot's token.
    updater = Updater(config['token'])

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("trein", trein, pass_args=True))

    dp.add_handler(InlineQueryHandler(inlinequery))

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()