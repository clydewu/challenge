# -*- coding: utf-8 -*-

from flask import current_app, g

from pymongo import MongoClient
from pymongo import InsertOne
from pymongo import DeleteMany

KEY_PREFIX = 'MASKY_'

KEY_DB_HOST = 'MASKY_DB_HOST'
KEY_DB_PORT = 'MASKY_DB_PORT'
KEY_DB_USERNAME = 'MASKY_DB_USERNAME'
KEY_DB_PASSWORD = 'MASKY_DB_PASSWORD'
KEY_DB_NAME = 'MASKY_DB_NAME'
KEY_DB_COLLECTION = 'MASKY_DB_COLLECTION'

# -- {key : (key, def_var, comment)}
DEF_CONF = {
    KEY_DB_HOST: (KEY_DB_HOST, 'localhost', 'Monogo db host'),
    KEY_DB_PORT: (KEY_DB_PORT, '27017', 'Mongo db port'),
    KEY_DB_USERNAME: (KEY_DB_USERNAME, '', 'Mongo db username'),
    KEY_DB_PASSWORD: (KEY_DB_PASSWORD, '', 'Mongo db password'),
    KEY_DB_NAME: (KEY_DB_NAME, 'masky', 'Mongo db name'),
    KEY_DB_COLLECTION: (KEY_DB_COLLECTION, 'fruits', 'Mongo db collection')
}


def initial(app):
    '''
    Initial this module into flask app

    @param app: The flask app
    '''
    app.teardown_appcontext(close_client)


def get_client():
    '''
    Return a MongoClient object

    @return: The MongoClient object
    '''
    if 'mongo_client' not in g:
        host = current_app.config[KEY_DB_HOST]
        port = int(current_app.config[KEY_DB_PORT]) if current_app.config[KEY_DB_PORT].isdigit() else None
        username = current_app.config[KEY_DB_USERNAME]
        password = current_app.config[KEY_DB_PASSWORD]
        name = current_app.config[KEY_DB_NAME]
        current_app.logger.info("MongoDB connection info, host: {}, port: {}, username: {}, password: {}, authSource: {}".format(
            host, port, username, password, name))
        g.mongo_client = MongoClient(host=host, port=port, username=username, password=password, authSource=name, tz_aware=True)

    return g.mongo_client


def close_client(*args, **kwargs):
    client = g.pop('mongo_client', None)

    if client is not None:
        client.close()


def gen_bulk_operations(iter, turncate=False):
    '''
    @param iter: The iterable object will be insert into DB.
    @param turncate: If True, a DeleteMany operation will be applied before other operations.
    @return: A list of BulkOperation subclass.
    '''

    return ([DeleteMany({})] if turncate else []) + \
        [InsertOne(r) for r in iter]
