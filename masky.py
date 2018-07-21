# -*- coding: utf-8 -*-
'''
'''
import os
from datetime import datetime

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
    import ipdb; ipdb.set_trace()
    df, modify_dt = _load_csv_to_df(file_path)
    collection = _get_collection('masky', 'fruits')
    add_dict = {'datetime': modify_dt.strftime('%Y-%m-%d %H:%M:%S')}
    input_dict = _df_2_dict(df)
    updated_dict = _add_dict_field(input_dict, add_dict)
    bulk_operations = _gen_bulk_operations(updated_dict, turncate)
    collection.bulk_write(bulk_operations)


def _load_csv_to_df(file_path):
    app.logger.info('Load {} ...'.format(file_path))
    df = pandas.read_csv(file_path, header=None, names=['id', 'name', 'price', 'amount'])
    modify_dt = datetime.fromtimestamp(os.stat(file_path).st_mtime)
    df.info()
    app.logger.info('Load CSV file ok, file_path: {}, modify time: {}.'.format(file_path, modify_dt))
    return df, modify_dt


def _get_collection(db_name, collection_name):
    return MongoClient()[db_name][collection_name]


def _df_2_dict(data_frame):
    '''
    @param data_frame: Input DataFrame
    @param additional_dict: The additional dictionary which will be added into each row
    @return: A list of BulkOperation subclass
    '''
    return [r[1].to_dict() for r in data_frame.iterrows()]


def _add_dict_field(input_dict, additional_dict):
    # -- Due to additional_dict is not in the scropt of map() or lambda, use for-loop instead of
    for d in input_dict:
        d.update(additional_dict)
    return input_dict


def _modify_dict_value(input_dict, action):
    return map(action, input_dict)


def _gen_bulk_operations(input_dict, turncate=False):
    '''
    @param input_dict: The dictionary will be insert into DB
    @return: A list of BulkOperation subclass
    '''
    return ([DeleteMany({})] if turncate else []) + [InsertOne(d) for d in input_dict]


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
