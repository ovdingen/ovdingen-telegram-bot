#!/usr/bin/env python

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging
import json
import datetime
import dvs

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


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

    treininfo = dvs.train("https://dvs.ovdingen.nl", date, treinnummer)
    
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
        
        mat_text = "*Materieel:*\n"
        if len(vleugel['mat']) is 0:
            mat_text += "Materieelinfo niet beschikbaar"
        else:
            for materieel in vleugel['mat']:
                if materieel[2] is None: # geen mat-nr
                    mat_text += "{}, eindbestemming {}".format(materieel[0], materieel[1])
                else:
                    mat_text += "{} {}, eindbestemming {}".format(materieel[0], materieel[2], materieel[1])
        


        vleugeltekst = stops + "\n" + mat_text
            

    
    message = header + vleugeltekst

    update.message.reply_text(message, parse_mode="Markdown")

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

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()