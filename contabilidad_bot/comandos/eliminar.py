from contabilidad_bot import connection, dispatcher, automata, config
from telegram.ext import CommandHandler, ConversationHandler, CallbackQueryHandler
import logging
from telegram.ext.dispatcher import run_async
from datetime import datetime
from bson.objectid import ObjectId
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram import KeyboardButton, ReplyKeyboardMarkup

logging.info("Agregando comando /eliminar")

@run_async
def eliminar(bot, update, args):
	logging.info("Llamado /eliminar")
	db_name = config.db['prefix'] + str(update.message.chat_id)
	collection = connection[db_name]['gastos']
	if len(args):
		_id = ObjectId(args[0])
		count = collection.delete_one({'_id': _id})
		ret_txt = 'Eliminado' if count else 'No encontrado'
		bot.send_message(chat_id=update.message.chat_id, text=ret_txt)
	else:
		gastos = collection.find()
		button_list = []
		for gasto in gastos:
			button_list.append([InlineKeyboardButton(str(gasto), callback_data=str(gasto['_id']))])
			#button_list.append([KeyboardButton(str(gasto))])
		ret_txt = 'Elija uno para eliminar'
		reply_markup = InlineKeyboardMarkup(button_list)
		#reply_markup = ReplyKeyboardMarkup(button_list)
		bot.send_message(chat_id=update.message.chat_id, text=ret_txt, reply_markup=reply_markup)

eliminar_handler = CommandHandler('eliminar', eliminar, pass_args=True)
dispatcher.add_handler(eliminar_handler)