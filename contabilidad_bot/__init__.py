from pymongo import MongoClient
from telegram.ext import Updater
import logging
from contabilidad_bot import config

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

logging.info("Conectando a la DB")
connection = MongoClient()

logging.info("Iniciando Telegram")
updater = Updater(config.telegram['token'])
dispatcher = updater.dispatcher

from telegram.error import (TelegramError, Unauthorized, BadRequest, 
                            TimedOut, ChatMigrated, NetworkError)

def error_callback(bot, update, error):
    try:
        raise error
    except Unauthorized:
        print("# remove update.message.chat_id from conversation list")
    except BadRequest:
        print("# handle malformed requests - read more below!")
    except TimedOut:
        print("# handle slow connection problems")
    except NetworkError:
        print("# handle other connection problems")
    except ChatMigrated as e:
        print("# the chat_id of a group has changed, use e.new_chat_id instead")
    except TelegramError:
        print("# handle all other telegram related errors")

dispatcher.add_error_handler(error_callback)

logging.info("Importando comandos:")
from contabilidad_bot.comandos import efectivo, eliminar

logging.info("Esperando mensajes...")
updater.start_polling()
