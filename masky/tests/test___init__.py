# -*- coding: utf-8 -*-
import pytest

from masky import create_app
from masky.mongo_db import DEF_CONF
from masky.mongo_db import KEY_DB_HOST
from masky.mongo_db import KEY_DB_PORT
from masky.mongo_db import KEY_DB_NAME
from masky.mongo_db import KEY_DB_COLLECTION


class TestMongoDB(object):
    def test_hello(self, client):
        response = client.get('/')
        assert response.data == b'Hello, World!'

    def test_create_app_configuration(self, monkeypatch):
        with monkeypatch.context() as ctx:
            ctx.setenv(KEY_DB_PORT, 'env_port')
            ctx.setenv(KEY_DB_NAME, 'env_name')
            ctx.setenv(KEY_DB_COLLECTION, 'env_collection')

            app = create_app({KEY_DB_NAME: 'param_name', KEY_DB_COLLECTION: 'param_collection'})
            assert app.config[KEY_DB_HOST] == DEF_CONF[KEY_DB_HOST][1]
            assert app.config[KEY_DB_PORT] == 'env_port'
            assert app.config[KEY_DB_NAME] == 'param_name'
            assert app.config[KEY_DB_COLLECTION] == 'param_collection'
