# -*- coding: utf-8 -*-

from flask import current_app, g

from pymongo import MongoClient
from pymongo import InsertOne
from pymongo import DeleteMany


KEY_DB_HOST = 'DB_HOST'
KEY_DB_PORT = 'DB_PORT'
KEY_DB_NAME = 'DB_NAME'
KEY_DB_COLLECTION = 'DB_COLLECTION'

# -- {key : (key, def_var, comment)}
DEF_CONF = {
    KEY_DB_HOST: (KEY_DB_HOST, 'localhost', 'Monogo db host'),
    KEY_DB_PORT: (KEY_DB_PORT, '27017', 'Mongo db port'),
    KEY_DB_NAME: (KEY_DB_NAME, 'masky', 'Mongo db name'),
    KEY_DB_COLLECTION: (KEY_DB_COLLECTION, 'fruits', 'Mongo db collection')
}


def initial(app):
    app.teardown_appcontext(close_client)


def get_client():
    if 'mongo_client' not in g:
        host = current_app.config[KEY_DB_HOST]
        port = int(current_app.config[KEY_DB_PORT]) if current_app.config[KEY_DB_PORT].isdigit() else None
        g.mongo_client = MongoClient(host=host, port=port, tz_aware=True)

    return g.mongo_client


def close_client(*args, **kwargs):
    client = g.pop('mongo_client', None)

    if client is not None:
        client.close()


def gen_bulk_operations(iter, turncate=False):
    '''
    @param iter: The iterable object will be insert into DB
    @return: A list of BulkOperation subclass
    '''

    return ([DeleteMany({})] if turncate else []) + \
        [InsertOne(r) for r in iter]
