from contabilidad_bot import dispatcher, dbmongo
from telegram.ext import CommandHandler, CallbackQueryHandler
import logging
from telegram.ext.dispatcher import run_async
from telegram import InlineKeyboardMarkup

logging.info("Agregando comando /listar")


@run_async
def listar(bot, update, args):
    logging.info("Llamado /listar")
    collection = dbmongo.get_collection(update.message.chat_id, 'gastos')
    button_list = dbmongo.listar_collection(collection, 'listar', limit=5)
    reply_markup = InlineKeyboardMarkup(button_list)
    update.message.reply_text('Listado de gastos:',
                              reply_markup=reply_markup)


listar_handler = CommandHandler('listar', listar, pass_args=True)
dispatcher.add_handler(listar_handler)


def listar_callback(bot, update):
    logging.info("listar_callback")
    query = update.callback_query
    args = query.data.split()
    collection = dbmongo.get_collection(query.message.chat_id, 'gastos')
    if args[1] == 'nav':
        button_list = dbmongo.listar_collection(collection,
                                                'listar',
                                                skip=int(args[2]),
                                                limit=int(args[3]))
        reply_markup = InlineKeyboardMarkup(button_list)
        bot.edit_message_text(text='Listado de gastos:',
                              chat_id=query.message.chat_id,
                              message_id=query.message.message_id,
                              reply_markup=reply_markup)

    else:
        bot.edit_message_text(text="Listado terminado",
                              chat_id=query.message.chat_id,
                              message_id=query.message.message_id)


dispatcher.add_handler(CallbackQueryHandler(listar_callback,
                                            pattern=r'\listar\s[\s\S]*'))
