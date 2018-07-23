# -*- coding: utf-8 -*-
'''
'''
import os

import ipdb

from flask import Flask

import click

import pandas
from pandas.api.types import is_string_dtype
from pandas.api.types import is_numeric_dtype

from pymongo import MongoClient
from pymongo import InsertOne
from pymongo import DeleteMany

app = Flask(__name__)


@app.cli.command('load', help='Load a csv file and save to mongoDB')
@click.argument('file_path', required=True)
@click.option('--turncate', '-t', type=bool, is_flag=True, help="Clear collection before reading")
def load(file_path, turncate):
    '''
    Saves the CSV file from a local directory path to MongoDB, with an additional date time field for when the csv file was saved

    @param file_path: The string file path of CSV file
    @param turncate: Whether clear up collection before insertion
    '''
    app.logger.info('Execute load command, file_path: {}, turncate: {}'.format(file_path, turncate))

    mtime = os.stat(file_path).st_mtime
    df = pandas.read_csv(file_path, header=None, names=['id', 'name', 'price', 'amount'])
    app.logger.info('Load CSV file ok, file_path: {}, mtime: {}'.format(file_path, mtime))

    df = _add_mtime(df, mtime)

    app.logger.info('Prepare write into DB, count: {}, turncate: {}'.format(df.shape[0], turncate))
    collection = MongoClient()['masky']['fruits']
    result = collection.bulk_write(_gen_bulk_operations(df.iterrows(), turncate))
    app.logger.info('Bulk write OK, nInserted: {nInserted}, nUpserted: {nUpserted}, nMatched: {nMatched}, '
                    'nModified: {nModified}, nRemoved: {nRemoved}, upserted: {upserted}'.format(**result.bulk_api_result))


@app.cli.command('alter', help='Alter a csv file and save to mongoDB')
@click.argument('file_path', required=True)
@click.option('--turncate', '-t', type=bool, is_flag=True, help="Clear collection before reading")
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
    ipdb.set_trace()
    df = _manipulate_data(df)

    app.logger.info('Prepare write into DB, turncate: {}, count: {}'.format(turncate, df.shape[0]))
    collection = MongoClient()['masky']['fruits']
    result = collection.bulk_write(_gen_bulk_operations([df.to_dict()]))
    app.logger.info('Bulk write OK, nInserted: {nInserted}, nUpserted: {nUpserted}, nMatched: {nMatched}, '
                    'nModified: {nModified}, nRemoved: {nRemoved}, upserted: {upserted}'.format(**result.bulk_api_result))


def _gen_bulk_operations(iter, turncate=False):
    '''
    @param iter: The dictionary will be insert into DB
    @return: A list of BulkOperation subclass
    '''
    return ([DeleteMany({})] if turncate else []) + \
        [InsertOne(r[1].to_dict()) for r in iter]


def _add_mtime(df, mtime):
    app.logger.info('Add additional time field, timestamp: {}'.format(mtime))
    df['mtime'] = mtime
    df['mtime'] = pandas.to_datetime(df['mtime'].astype(int), unit='s')
    return df


def _manipulate_data(df):
    app.logger.info('Manipulate data...')
    df = df.apply(lambda x: x.str.upper() if is_string_dtype(x) else x.apply(lambda x: x + 1) if is_numeric_dtype(x) else x)
    df.index = df.index.astype(str)
    return df
