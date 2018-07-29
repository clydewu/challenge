# -*- coding: utf-8 -*-
import os

from flask import Flask

from . import mongo_db
from .mongo_db import DEF_CONF
from . import fruits


def create_app(test_config={}):
    '''
    A factory method which return a flask app.

    @param test_config: It will overwrite app.config with the highest priority
    @return: The priority of configuration is:
        1. Hard-coding default
        2. Environment variable
        3. Paramaters of create_app()
    '''
    app = Flask(__name__, instance_relative_config=True)

    # -- Load conf from default
    app.config.update({c[0]: c[1] for c in DEF_CONF.values()})
    # -- Load conf from environment variable
    app.config.update({c[0]: os.environ.get(c[0]) for c in DEF_CONF.values() if os.environ.get(c[0])})
    # -- Load conf from paramaters
    app.config.update(test_config)

    @app.route('/')
    def hello():
        return 'Hello, World!'

    fruits.initial(app)
    mongo_db.initial(app)

    return app
