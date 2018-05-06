from bot_text import treinToText, stationToText
import datetime
import dvs
from uuid import uuid4
from telegram import InlineQueryResultArticle, InputTextMessageContent

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

def station(bot, update, args):
    if len(args) > 1:
        update.message.reply_text("Too many arguments. Try using /help.")
        return False
    if len(args) is 0:
        update.message.reply_text("Too few arguments. Try using /help.")
        return False
    
    stationcode = args[0]


    station = dvs.station("https://dvs.ovdingen.nl", stationcode)

    message = stationToText(station)
    

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