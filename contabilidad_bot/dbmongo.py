from contabilidad_bot import config, connection
import pymongo
import arrow
from telegram import InlineKeyboardButton


def get_collection(chat_id, collection):
    db_name = config.db['prefix'] + str(chat_id)
    collection = connection[db_name][collection]
    return collection


def listar_collection(collection, comando,
                      sort=["creacion", pymongo.ASCENDING],
                      limit=10, skip=0):
    button_list = []
    objects = collection.find().sort(*sort).skip(skip).limit(limit)
    for o in objects:
        texto = formats[collection.name](o)
        callback_data = comando + str(o['_id'])
        button_list.append(
            [InlineKeyboardButton(texto,
                                  callback_data=callback_data)])
    nav = []
    if skip:
        texto = '<< Anteriores'
        callback_data = '{0} nav {1} {2}'.format(comando, skip - limit, limit)
        nav.append(InlineKeyboardButton(texto,
                                        callback_data=callback_data))
    # Si hay mas
    if (skip + len(button_list)) < collection.count():
        texto = 'Siguientes >>'
        callback_data = '{0} nav {1} {2}'.format(comando, skip + limit, limit)
        nav.append(InlineKeyboardButton(texto,
                                        callback_data=callback_data))

    if len(nav):
        button_list.append(nav)

    return button_list


def format_gasto(gasto):
    gasto['fecha_humana'] = arrow.get(gasto['creacion']).humanize(locale='es')
    gasto['tags_humana'] = ' '.join(gasto['tags'])
    formato = '{fecha_humana} {descripcion} {importe} {tags_humana}'
    return formato.format_map(gasto)


formats = {
    'gastos': format_gasto
}
