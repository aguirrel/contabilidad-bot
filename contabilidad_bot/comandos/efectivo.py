from contabilidad_bot import connection, dispatcher, automata, config, dbmongo
from telegram.ext import CommandHandler
import logging
from telegram.ext.dispatcher import run_async
from datetime import datetime

NUMBER = r'\d+[.]*\d*'
WORD = r'[a-zA-Z_][a-zA-Z0-9_]*'
TAG = r'#[a-zA-Z0-9_]*'
END = r'\0'

GRAPH_ADD_PAYMENT = {
    's': {WORD: 'a', NUMBER: None, TAG: None, END: None},
    'a': {WORD: 'a', NUMBER: 'b', TAG: None, END: None},
    'b': {WORD: None, NUMBER: None, TAG: 'c', END: 'f'},
    'c': {WORD: None, NUMBER: None, TAG: 'c', END: 'f'},
    'f': {WORD: None, NUMBER: None, TAG: None, END: None}
}

ACTIONS_ADD_PAYMENT = {
    's': lambda d, o: None,
    'a': lambda d, o: d.setdefault('descripcion', []).append(o),
    'b': lambda d, o: d.update({'importe': o}),
    'c': lambda d, o: d.setdefault('tags', []).append(o),
    'f': lambda d, o: None
}

logging.info("Agregando comando /efectivo")


@run_async
def efectivo(bot, update, args):
    ret_txt = ""
    args.append('\0')
    resultado = {'descripcion': [], 'importe': '0', 'tags': []}
    ret = automata.process(args, GRAPH_ADD_PAYMENT, 's',
                           ACTIONS_ADD_PAYMENT, resultado)

    if(ret):
        resultado['descripcion'] = ' '.join(resultado['descripcion'])
        resultado['creacion'] = datetime.utcnow()
        resultado['tipo'] = 'efectivo'
        resultado['importe'] = float(resultado['importe'])
        collection = dbmongo.get_collection(update.message.chat_id, 'gastos')
        collection.insert_one(resultado)
        ret_txt = 'Cobro contabilizado: ' + resultado['descripcion'] + \
                  '\nimporte: ' + resultado['importe'] + \
                  '\ntags: ' + ' '.join(resultado['tags'])
    else:
        ret_txt = '''/efectivo - Agrega un gasto en efectivo,
        el formato es: descripción importe tags (con # adelante),
        ej: almacén 134.34 #comida #gasto_corriente'''
    bot.send_message(chat_id=update.message.chat_id, text=ret_txt)


efectivo_handler = CommandHandler('efectivo', efectivo, pass_args=True)
dispatcher.add_handler(efectivo_handler)
