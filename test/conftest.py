# -*- coding: utf-8 -*-

import os
import csv
import tempfile

import pytest


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

    return _csv_generator
