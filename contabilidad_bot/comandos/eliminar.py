from contabilidad_bot import dispatcher, dbmongo
from telegram.ext import CommandHandler, CallbackQueryHandler
import logging
from telegram.ext.dispatcher import run_async
from bson.objectid import ObjectId
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
import arrow

logging.info("Agregando comando /eliminar")


@run_async
def eliminar(bot, update, args):
    logging.info("Llamado /eliminar")
    collection = dbmongo.get_collection(update.message.chat_id, 'gastos')
    gastos = collection.find()
    button_list = []
    for gasto in gastos:
        callback_data = 'eliminar ' + str(gasto['_id'])
        fecha = arrow.get(gasto['creacion'])
        texto = fecha.humanize(locale='es') + \
            ' ' + gasto['descripcion'] + ' ' + str(gasto['importe'])
        button_list.append(
            [InlineKeyboardButton(texto,
                                  callback_data=callback_data)])
    reply_markup = InlineKeyboardMarkup(button_list)
    update.message.reply_text('Elija cual eliminar:',
                              reply_markup=reply_markup)


eliminar_handler = CommandHandler('eliminar', eliminar, pass_args=True)
dispatcher.add_handler(eliminar_handler)


def eliminar_callback(bot, update):
    query = update.callback_query
    args = query.data.split()
    _id = ObjectId(args[1])

    collection = dbmongo.get_collection(query.message.chat_id, 'gastos')
    count = collection.delete_one({'_id': _id})

    ret_txt = 'Eliminado' if count else 'No encontrado'
    bot.edit_message_text(text=ret_txt,
                          chat_id=query.message.chat_id,
                          message_id=query.message.message_id)


dispatcher.add_handler(CallbackQueryHandler(eliminar_callback,
                                            pattern=r'\eliminar\s[\s\S]*'))
