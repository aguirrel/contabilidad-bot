from contabilidad_bot import dispatcher, dbmongo
from telegram.ext import CommandHandler, CallbackQueryHandler
import logging
from telegram.ext.dispatcher import run_async
from bson.objectid import ObjectId
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

logging.info("Agregando comando /eliminar")


@run_async
def eliminar(bot, update, args):
    logging.info("Llamado /eliminar")
    collection = dbmongo.get_collection(update.message.chat_id, 'gastos')
    button_list = dbmongo.listar_collection(collection, 'eliminar', limit=5)
    reply_markup = InlineKeyboardMarkup(button_list)
    update.message.reply_text('Elija cual eliminar:',
                              reply_markup=reply_markup)


eliminar_handler = CommandHandler('eliminar', eliminar, pass_args=True)
dispatcher.add_handler(eliminar_handler)


def eliminar_callback(bot, update):
    logging.info("eliminar_callback")
    query = update.callback_query
    args = query.data.split()
    collection = dbmongo.get_collection(query.message.chat_id, 'gastos')

    if args[1] == 'nav':
        button_list = dbmongo.listar_collection(collection,
                                                'eliminar',
                                                skip=int(args[2]),
                                                limit=int(args[3]))
        reply_markup = InlineKeyboardMarkup(button_list)
        bot.edit_message_text(text='Elija cual eliminar:',
                              chat_id=query.message.chat_id,
                              message_id=query.message.message_id,
                              reply_markup=reply_markup)
    else:
        _id = ObjectId(args[1])
        o = collection.find_one({'_id': _id})
        if o:
            button_list = []
            str_gasto = dbmongo.format_gasto(o)
            logging.info(str_gasto)
            button_list.append([
                InlineKeyboardButton(str_gasto,
                                     callback_data='confeliminar cancelar')])
            conf_button = []
            conf_button.append(
                InlineKeyboardButton("Eliminar",
                                     callback_data='confeliminar ' + str(_id)))
            conf_button.append(
                InlineKeyboardButton(
                    "Cancelar", callback_data='confeliminar cancelar'))
            button_list.append(conf_button)
            reply_markup = InlineKeyboardMarkup(button_list)
            bot.edit_message_text(text='Confirmar eliminación:',
                                  chat_id=query.message.chat_id,
                                  message_id=query.message.message_id,
                                  reply_markup=reply_markup)
        else:
            bot.edit_message_text(text='Gasto no encontrado',
                                  chat_id=query.message.chat_id,
                                  message_id=query.message.message_id)


def confirmar_eliminar_callback(bot, update):
    logging.info("confirmar_eliminar_callback")
    query = update.callback_query
    args = query.data.split()
    if args[1] == 'cancelar':
        bot.edit_message_text(text='Eliminación cancelada',
                              chat_id=query.message.chat_id,
                              message_id=query.message.message_id)
    else:
        _id = ObjectId(args[1])
        collection = dbmongo.get_collection(query.message.chat_id, 'gastos')
        count = collection.delete_one({'_id': _id})
        ret_txt = 'Eliminado' if count else 'No encontrado'
        bot.edit_message_text(text=ret_txt,
                              chat_id=query.message.chat_id,
                              message_id=query.message.message_id)


dispatcher.add_handler(CallbackQueryHandler(eliminar_callback,
                                            pattern=r'\eliminar\s[\s\S]*'))
dispatcher.add_handler(CallbackQueryHandler(confirmar_eliminar_callback,
                                            pattern=r'\confeliminar\s[\s\S]*'))
