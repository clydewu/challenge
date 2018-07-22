# -*- coding: utf-8 -*-
'''
'''
import os

import ipdb

from flask import Flask

import click

import pandas

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

    @param file_name: The string file path of CSV file
    @param turncate: Whether clear up collection before insertion
    '''
    app.logger.info('Execute load command, file_path: {}, turncate: {}'.format(file_path, turncate))
    collection = MongoClient()['masky']['fruits']
    mtime = os.stat(file_path).st_mtime
    df = pandas.read_csv(file_path, header=None, names=['id', 'name', 'price', 'amount'])
    app.logger.info('Load CSV file ok, file_path: {}, mtime: {}'.format(file_path, mtime))

    app.logger.info('Add additional time field, timestamp: {}'.format(mtime))
    df['mtime'] = mtime
    df['mtime'] = pandas.to_datetime(df['mtime'].astype(int), unit='s')

    app.logger.info('Prepare write into DB, count: {}, turncate: {}'.format(df.shape[0], turncate))
    bulk_operations = _gen_bulk_operations(df, turncate)
    collection.bulk_write(bulk_operations)


def _gen_bulk_operations(date_frame, turncate=False):
    '''
    @param date_frame: The dictionary will be insert into DB
    @return: A list of BulkOperation subclass
    '''
    return ([DeleteMany({})] if turncate else []) + \
        [InsertOne(r[1].to_dict()) for r in date_frame.iterrows()]


@app.cli.command('alter', help='Alter a csv file and save to mongoDB')
@click.argument('file_name', required=True)
@click.option('--turncate', '-t', type=bool, default=False, help="Clear collection before reading")
def alter(file_name):
    '''
    Manipulates the original csv and saves the altered csv file in a new mongo document. The csv should be manipulated as follows:
    1. All characters in columns with string type should be capitalized.
    2. All columns with floats/integers should be incremented by 1

    @param file_name: the string file path of CSV file
    '''
    pass
