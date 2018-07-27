# -*- coding: utf-8 -*-

import pytest
from pymongo import InsertOne
from pymongo import DeleteMany

from masky import mongo_db


class TestMongoDB(object):
    def test_initial(self, app):
        with app.app_context():
            assert mongo_db.close_client in app.teardown_appcontext_funcs

    def test_get_client(self, app):
        with app.app_context():
            client = mongo_db.get_client()
            assert client is mongo_db.get_client()

    @pytest.mark.skip(reason='There is no way to check close or not')
    def test_close_client(self, app):
        with app.app_context():
            client = mongo_db.get_client()
            client.close()
            mongo_db.close_client()

    # @pytest.mark.skip(reason='test')
    def test_gen_bulk_operations_wout_t(self):
        input_iter = [{'id': 3}, {'id': 4}]
        expected = [InsertOne({'id': 3}), InsertOne({'id': 4})]

        result = mongo_db.gen_bulk_operations(input_iter)
        assert result == expected

    # @pytest.mark.skip(reason='test')
    def test_gen_bulk_operations_with_t(self):
        input_iter = [{'id': 3}, {'id': 4}]
        expected = [DeleteMany({}), InsertOne({'id': 3}), InsertOne({'id': 4})]

        result = mongo_db.gen_bulk_operations(input_iter, turncate=True)
        assert result == expected
