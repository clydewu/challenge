# -*- coding: utf-8 -*-
import os
import ipdb

from flask import Flask

# !!!TODO!!!, Why the dot is necessary
from .mongo_conf import DEF_CONF
from . import fruits


ipdb = ipdb  # -- This is just I don't want to see warning of unused variable


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)

    # -- Load db conf, first use value from env then use default value
    for conf in DEF_CONF:
        app.config[conf[0]] = os.environ.get(*conf)

    fruits.init_app(app)

    return app
