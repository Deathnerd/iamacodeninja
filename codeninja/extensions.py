# -*- coding: utf-8 -*-
from flask import request
"""
All of our extensions are initialized here. They are registered in
app.py:register_extensions upon app creation
"""
from flask.ext.sqlalchemy import SQLAlchemy
db = SQLAlchemy()

from flask.ext.migrate import Migrate
migrate = Migrate()

from flask.ext.debugtoolbar import DebugToolbarExtension
debug_toolbar = DebugToolbarExtension()

from flask.ext.bcrypt import Bcrypt
bcrypt = Bcrypt()

from flask.ext.admin import Admin
admin = Admin(name="I am a Code Ninja!", template_mode='bootstrap3')

from flask.ext.login import LoginManager
login_manager = LoginManager()

from flask.ext.assets import Environment
assets = Environment()