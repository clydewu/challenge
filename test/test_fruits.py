# -*- coding: utf-8 -*-
'''
Testing for Masky
'''

import pytest
from src import masky
from pymongo import InsertOne
from pymongo import DeleteMany


class TestFruits(object):
    def test_load_wout_t(self, csv_generator):
        csv_path = csv_generator([[1, 2, 3], [4, 5, 6]])
        cmd_runner = masky.app.test_cli_runner()
        result = cmd_runner.invoke(args=['load', csv_path])

    def test_load_with_t(self):
        pass

    def test_alter_with_t(self):
        pass

    def test_alter_wout_t(self):
        pass

    @pytest.mark.skip(reason='test')
    def test_gen_bulk_operations_turncate_false(self):
        input_iter = [{'id': 3}, {'id': 4}]
        expected = [InsertOne({'id': 3}), InsertOne({'id': 4})]

        result = masky._gen_bulk_operations(input_iter)
        assert result == expected

    @pytest.mark.skip(reason='test')
    def test_gen_bulk_operations_turncate_true(self):
        input_iter = [{'id': 3}, {'id': 4}]
        expected = [DeleteMany({}), InsertOne({'id': 3}), InsertOne({'id': 4})]

        result = masky._gen_bulk_operations(input_iter, turncate=True)
        assert result == expected

    def test_add_mtime(self):
        pass

    def test_manipulate_data(self):
        pass
