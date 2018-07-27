# -*- coding: utf-8 -*-
'''
Testing for Masky
'''
import os
from datetime import datetime
import time

import pytest
import pandas
from pandas.util.testing import assert_frame_equal
from pandas import Timestamp
import pytz
from tzlocal import get_localzone

from masky import fruits
from masky import mongo_db
from masky.mongo_db import KEY_DB_NAME
from masky.mongo_db import KEY_DB_COLLECTION


LOCAL_TZ = get_localzone()


class TestFruits(object):
    # @pytest.mark.skip(reason='test')
    def test_load_wout_t(self, app, runner, csv_generator):
        # -- Prepare input and expected data
        test_input = [['1021', 'Guava', '1', '160'], ['1022', 'Huckleberry', '6', '197'], ['1023', 'Jackfruit', '6', '181']]
        csv_path = csv_generator(test_input)
        csv_dt = csv_dt = self.__get_csv_mtime_dt(csv_path)
        expected_output = [[1021, 'Guava', 1, 160, csv_dt], [1022, 'Huckleberry', 6, 197, csv_dt], [1023, 'Jackfruit', 6, 181, csv_dt]]

        # -- Run
        runner.invoke(args=['load', csv_path])

        # -- Get result and do assert
        result_docs = self.__get_documents(app)
        assert self.__is_expected_load_results(result_docs, expected_output)

    # @pytest.mark.skip(reason='test')
    def test_load_wout_t_twice(self, app, runner, csv_generator):
        test_input = [['1021', 'Guava', '1', '160'], ['1022', 'Huckleberry', '6', '197'], ['1023', 'Jackfruit', '6', '181']]
        csv_path = csv_generator(test_input)
        csv_dt = self.__get_csv_mtime_dt(csv_path)
        expected_output = [[1021, 'Guava', 1, 160, csv_dt], [1022, 'Huckleberry', 6, 197, csv_dt], [1023, 'Jackfruit', 6, 181, csv_dt]]
        expected_output += expected_output  # -- Duplicate expected result here

        # -- Run load twice
        runner.invoke(args=['load', csv_path])
        runner.invoke(args=['load', csv_path])

        result_docs = self.__get_documents(app)
        assert self.__is_expected_load_results(result_docs, expected_output)

    # @pytest.mark.skip(reason='test')
    def test_load_with_t(self, app, runner, csv_generator):
        test_input = [['1021', 'Guava', '1', '160'], ['1022', 'Huckleberry', '6', '197'], ['1023', 'Jackfruit', '6', '181']]
        csv_path = csv_generator(test_input)
        csv_dt = self.__get_csv_mtime_dt(csv_path)
        expected_output = [[1021, 'Guava', 1, 160, csv_dt], [1022, 'Huckleberry', 6, 197, csv_dt], [1023, 'Jackfruit', 6, 181, csv_dt]]

        runner.invoke(args=['load', '-t', csv_path])

        result_docs = self.__get_documents(app)
        assert self.__is_expected_load_results(result_docs, expected_output)

    # @pytest.mark.skip(reason='test')
    def test_load_with_t_twice(self, app, runner, csv_generator):
        test_input = [['1021', 'Guava', '1', '160'], ['1022', 'Huckleberry', '6', '197'], ['1023', 'Jackfruit', '6', '181']]
        csv_path = csv_generator(test_input)
        csv_dt = self.__get_csv_mtime_dt(csv_path)
        expected_output = [[1021, 'Guava', 1, 160, csv_dt], [1022, 'Huckleberry', 6, 197, csv_dt], [1023, 'Jackfruit', 6, 181, csv_dt]]

        runner.invoke(args=['load', '-t', csv_path])
        runner.invoke(args=['load', '-t', csv_path])

        result_docs = self.__get_documents(app)
        assert self.__is_expected_load_results(result_docs, expected_output)

    # @pytest.mark.skip(reason='test')
    def test_alter_wout_t(self, app, runner, csv_generator):
        test_input = [['1021', 'Guava', '1', '160'], ['1022', 'Huckleberry', '6', '197'], ['1023', 'Jackfruit', '6', '181']]
        csv_path = csv_generator(test_input)
        csv_dt = self.__get_csv_mtime_dt(csv_path)
        expected_output = [[[1022, 'GUAVA', 2, 161, csv_dt], [1023, 'HUCKLEBERRY', 7, 198, csv_dt], [1024, 'JACKFRUIT', 7, 182, csv_dt]]]

        runner.invoke(args=['alter', csv_path])

        result_docs = self.__get_documents(app)
        assert self.__is_expected_alter_results(result_docs, expected_output)

    # @pytest.mark.skip(reason='test')
    def test_alter_wout_t_twice(self, app, runner, csv_generator):
        test_input = [['1021', 'Guava', '1', '160'], ['1022', 'Huckleberry', '6', '197'], ['1023', 'Jackfruit', '6', '181']]
        csv_path = csv_generator(test_input)
        csv_dt = self.__get_csv_mtime_dt(csv_path)
        expected_output = [[[1022, 'GUAVA', 2, 161, csv_dt], [1023, 'HUCKLEBERRY', 7, 198, csv_dt], [1024, 'JACKFRUIT', 7, 182, csv_dt]]]
        expected_output += expected_output

        runner.invoke(args=['alter', csv_path])
        runner.invoke(args=['alter', csv_path])

        result_docs = self.__get_documents(app)
        assert self.__is_expected_alter_results(result_docs, expected_output)

    # @pytest.mark.skip(reason='test')
    def test_alter_with_t(self, app, runner, csv_generator):
        test_input = [['1021', 'Guava', '1', '160'], ['1022', 'Huckleberry', '6', '197'], ['1023', 'Jackfruit', '6', '181']]
        csv_path = csv_generator(test_input)
        csv_dt = self.__get_csv_mtime_dt(csv_path)
        expected_output = [[[1022, 'GUAVA', 2, 161, csv_dt], [1023, 'HUCKLEBERRY', 7, 198, csv_dt], [1024, 'JACKFRUIT', 7, 182, csv_dt]]]

        runner.invoke(args=['alter', '-t', csv_path])

        result_docs = self.__get_documents(app)
        assert self.__is_expected_alter_results(result_docs, expected_output)

    # @pytest.mark.skip(reason='test')
    def test_alter_with_t_twice(self, app, runner, csv_generator):
        test_input = [['1021', 'Guava', '1', '160'], ['1022', 'Huckleberry', '6', '197'], ['1023', 'Jackfruit', '6', '181']]
        csv_path = csv_generator(test_input)
        csv_dt = self.__get_csv_mtime_dt(csv_path)
        expected_output = [[[1022, 'GUAVA', 2, 161, csv_dt], [1023, 'HUCKLEBERRY', 7, 198, csv_dt], [1024, 'JACKFRUIT', 7, 182, csv_dt]]]

        runner.invoke(args=['alter', '-t', csv_path])
        runner.invoke(args=['alter', '-t', csv_path])

        result_docs = self.__get_documents(app)
        assert self.__is_expected_alter_results(result_docs, expected_output)

    # @pytest.mark.skip(reason='test')
    def test_add_mtime(self, app):
        input_amount = 10
        test_input = pandas.DataFrame({'seq': range(0, input_amount)})
        test_mtime = int(time.time())
        expected_mtime = Timestamp.fromtimestamp(test_mtime).tz_localize(LOCAL_TZ).tz_convert(pytz.UTC).replace(tzinfo=None)

        with app.app_context():
            result = fruits._add_mtime(test_input, test_mtime)

        assert len(result[result['mtime'] == expected_mtime]) == input_amount

    # @pytest.mark.skip(reason='test')
    def test_manipulate_data(self, app):
        test_input = pandas.DataFrame({'float': [0.45, 100.23], 'int': [199, 256], 'str': ['test_str_1', 'test_str_2']}, index=['a', 'b'])
        expected_output = pandas.DataFrame({'float': [1.45, 101.23], 'int': [200, 257], 'str': ['TEST_STR_1', 'TEST_STR_2']}, index=['a', 'b'])

        with app.app_context():
            result = fruits._manipulate_data(test_input)

        assert_frame_equal(result, expected_output)

    def __get_csv_mtime_dt(self, csv_path):
        return self.__ts_2_dt(int(os.stat(csv_path).st_mtime))

    def __ts_2_dt(self, ts):
        return LOCAL_TZ.localize(datetime.fromtimestamp(ts)).astimezone(pytz.UTC)

    def __get_documents(self, app):
        with app.app_context():
            client = mongo_db.get_client()
            collection = client[app.config[KEY_DB_NAME]][app.config[KEY_DB_COLLECTION]]
            docs = [d for d in collection.find()]

        return docs

    def __is_expected_load_results(self, result_docs, expected_output):
        assert len(result_docs) == len(expected_output)
        for i in range(0, len(result_docs)):
            if not (self.__is_expected_result(result_docs[i], expected_output[i]) and
                    result_docs[i]['mtime'] == expected_output[i][4]):
                return False
        return True

    def __is_expected_alter_results(self, result_docs, expected_output):
        assert len(result_docs) == len(expected_output)
        for i in range(0, len(result_docs)):
            del result_docs[i]['_id']
            assert len(result_docs[i]) == len(expected_output[i])
            doc_list = [d[1] for d in result_docs[i].items()]
            for j in range(0, len(doc_list)):
                if not self.__is_expected_result(doc_list[j], expected_output[i][j]):
                    return False
        return True

    def __is_expected_result(self, result, expected):
        return True if result['id'] == expected[0] and \
            result['name'] == expected[1] and \
            result['price'] == expected[2] and \
            result['amount'] == expected[3] else False
