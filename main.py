import telegram
from telegram.ext import Updater

bot = telegram.Bot(token='204509195:AAHYQPnz5ytWVBkZQA5nbZSn97Fqp_J2IEE')

updater = Updater(token='204509195:AAHYQPnz5ytWVBkZQA5nbZSn97Fqp_J2IEE')
dispatcher = updater.dispatcher

import logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',level=logging.INFO)




currentUser = 0
currentMax = 0

activeUsers = []
userChatIds = dict()



# list of functions and associated handlers


# /start
def start(bot, update):
    bot.sendMessage(chat_id=update.message.chat_id, text="Yo! Here's what you can do \n /requestNumber request a number\n /status see the current number")

from telegram.ext import CommandHandler
start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)




def requestNumber(bot, update):
    global currentMax
    currentMax = currentMax + 1

    bot.sendMessage(chat_id=update.message.chat_id, text="Your number is " + str(currentMax) )
    activeUsers.append(currentMax)
    userChatIds[currentMax] = update.message.chat_id

from telegram.ext import CommandHandler
requestNumber_handler = CommandHandler('requestNumber', requestNumber)
dispatcher.add_handler(requestNumber_handler)



def status(bot, update):
    bot.sendMessage(chat_id=update.message.chat_id, text="The current number is " + str(currentUser) )

from telegram.ext import CommandHandler
status_handler = CommandHandler('status', status)
dispatcher.add_handler(status_handler)


def nextUser(bot, update):
    global currentUser
    currentUser = activeUsers.pop(0)

    # notfiy current user
    bot.sendMessage(chat_id=userChatIds[currentUser], text=" User " + str(currentUser) + ", its your turn!")

    # notify users
    for i in activeUsers:
        bot.sendMessage(chat_id=userChatIds[i], text=" Current number is " + str(currentUser) + ". Still " + str(i - currentUser) + " people ahead of you.")

nextUser_handler = CommandHandler('nextUser', nextUser)
dispatcher.add_handler(nextUser_handler)






# list of functions and associated handlers




# echoing
def echo(bot, update):
    bot.sendMessage(chat_id=update.message.chat_id, text=update.message.text)

from telegram.ext import MessageHandler, Filters
echo_handler = MessageHandler([Filters.text], echo)
dispatcher.add_handler(echo_handler)

# caps
def caps(bot, update, args):
     text_caps = ' '.join(args).upper()
     bot.sendMessage(chat_id=update.message.chat_id, text=text_caps)


caps_handler = CommandHandler('caps', caps, pass_args=True)
dispatcher.add_handler(caps_handler)



from telegram import InlineQueryResultArticle, InputTextMessageContent
def inline_caps(bot, update):
    query = update.inline_query.query
    if not query:
        return
    results = list()
    results.append(
        InlineQueryResultArticle(
             id=query.upper(),
             title='Caps',
             input_message_content=InputTextMessageContent(query.upper())
        )
    )
    bot.answerInlineQuery(update.inline_query.id, results)

from telegram.ext import InlineQueryHandler
inline_caps_handler = InlineQueryHandler(inline_caps)
dispatcher.add_handler(inline_caps_handler)


updater.start_polling()