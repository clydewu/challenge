# -*- coding: utf-8 -*-
'''
'''
import os

import click

from flask import current_app as app
from flask.cli import with_appcontext

import pandas
from pandas.api.types import is_string_dtype
from pandas.api.types import is_numeric_dtype

from . import mongo_db
from .mongo_db import KEY_DB_NAME
from .mongo_db import KEY_DB_COLLECTION


def initial(app):
    '''
    Initial this module into flask app

    @param app: The flask app
    '''
    app.cli.add_command(load)
    app.cli.add_command(alter)


@click.command('load', help='Load a csv file and save to mongoDB')
@click.argument('file_path', required=True)
@click.option('--turncate', '-t', type=bool, is_flag=True, help="Clear collection before reading")
@with_appcontext
def load(file_path, turncate):
    '''
    Saves the CSV file from a local directory path to MongoDB, with an additional date time field for when the csv file was saved

    @param file_path: The string file path of CSV file
    @param turncate: Whether clear up collection before insertion
    '''
    # import ipdb; ipdb.set_trace()
    app.logger.info('Execute load command, file_path: {}, turncate: {}'.format(file_path, turncate))

    mtime = os.stat(file_path).st_mtime
    df = pandas.read_csv(file_path, header=None, names=['id', 'name', 'price', 'amount'])
    app.logger.info('Load CSV file ok, file_path: {}, mtime: {}'.format(file_path, mtime))

    df = _add_mtime(df, mtime)

    app.logger.info('Prepare write into DB, count: {}, turncate: {}'.format(df.shape[0], turncate))
    collection = mongo_db.get_client()[app.config[KEY_DB_NAME]][app.config[KEY_DB_COLLECTION]]
    result = collection.bulk_write(mongo_db.gen_bulk_operations([d[1].to_dict() for d in df.iterrows()], turncate))
    app.logger.info('Bulk write OK, nInserted: {nInserted}, nUpserted: {nUpserted}, nMatched: {nMatched}, '
                    'nModified: {nModified}, nRemoved: {nRemoved}, upserted: {upserted}'.format(**result.bulk_api_result))


@click.command('alter', help='Alter a csv file and save to mongoDB')
@click.argument('file_path', required=True)
@click.option('--turncate', '-t', type=bool, is_flag=True, help="Clear collection before reading")
@with_appcontext
def alter(file_path, turncate):
    '''
    Manipulates the original csv and saves the altered csv file in a new mongo document. The csv should be manipulated as follows:
    1. All characters in columns with string type should be capitalized.
    2. All columns with floats/integers should be incremented by 1

    @param file_path: The string file path of CSV file
    @param turncate: Whether clear up collection before insertion
    '''
    app.logger.info('Execute alter command, file_path: {}, turncate: {}'.format(file_path, turncate))

    df = pandas.read_csv(file_path, header=None, names=['id', 'name', 'price', 'amount'])
    app.logger.info('Load CSV file ok, file_path: {}'.format(file_path))
    df = _manipulate_data(df)

    app.logger.info('Prepare write into DB, turncate: {}, count: {}'.format(turncate, df.shape[0]))
    collection = mongo_db.get_client()[app.config[KEY_DB_NAME]][app.config[KEY_DB_COLLECTION]]

    result = collection.bulk_write(mongo_db.gen_bulk_operations([df.T.to_dict()], turncate))
    app.logger.info('Bulk write OK, nInserted: {nInserted}, nUpserted: {nUpserted}, nMatched: {nMatched}, '
                    'nModified: {nModified}, nRemoved: {nRemoved}, upserted: {upserted}'.format(**result.bulk_api_result))


def _add_mtime(df, mtime):
    '''
    Add a time field into a DataFrame

    @param df: Input DataFrame.
    @param mtime: A integer which represent a UNIX timestmp.
    @return: The the object as df.
    '''
    app.logger.info('Add additional time field, timestamp: {}'.format(mtime))
    df['mtime'] = mtime
    df['mtime'] = pandas.to_datetime(df['mtime'].astype(int), unit='s')
    return df


def _manipulate_data(df):
    '''
    Do the specified operation in the input DataFrame

    @param df: Input DataFrame.
    @return: The the object as df.
    '''
    app.logger.info('Manipulate data...')
    df = df.apply(lambda x: x.str.upper() if is_string_dtype(x) else x.apply(lambda x: x + 1) if is_numeric_dtype(x) else x)
    df.index = df.index.astype(str)
    return df
