# -*- coding: utf-8 -*-

import os
import csv
import tempfile

from masky import create_app

import pytest

from masky.mongo_db import DEF_CONF
from masky.mongo_db import KEY_DB_NAME
from masky.mongo_db import get_client


def pytest_addoption(parser):
    for conf in DEF_CONF.values():
        parser.addoption('--%s' % (conf[0].lower()), dest=conf[0], action='store', help=conf[2])


@pytest.fixture
def app(request):
    test_config = {'TESTING': True}

    for conf in DEF_CONF.values():
        conf_val = request.config.getoption(conf[0], None)
        if conf_val:
            test_config[conf[0]] = conf_val

    app = create_app(test_config)

    db_name = app.config[KEY_DB_NAME]
    with app.app_context():
        client = get_client()
        if db_name in client.list_database_names():
            raise Exception('The same name of DB is existent, name: {}'.format(db_name))

    def fin():
        client.drop_database(db_name)

    request.addfinalizer(fin)

    yield app


@pytest.fixture
def runner(app):
    yield app.test_cli_runner()


@pytest.fixture()
def csv_generator(request):
    file_fd, file_path = tempfile.mkstemp(text=True)
    csv_file = os.fdopen(file_fd, 'w')

    def _csv_generator(data):
        csv_writer = csv.writer(csv_file, quoting=csv.QUOTE_ALL, dialect=csv.Dialect.doublequote)
        csv_writer.writerows(data)
        csv_file.flush()
        return file_path

    def fin():
        csv_file.close()
        os.unlink(file_path)

    request.addfinalizer(fin)

    yield _csv_generator
