# -*- coding: utf-8 -*-
import os
from flask.ext.script import Manager, Shell, Server
from flask.ext.migrate import MigrateCommand
from codeninja.app import create_app, db
from codeninja.settings import Production, Development, Staging
from codeninja.models import User, Profile, Template
from flask import g
from flask.ext.login import current_user

if os.environ.get("CODENINJA_SERVER_ENV") == "prod":
    app = create_app(Production)
elif os.environ.get("CODENINJA_SERVER_ENV") == "staging":
    app = create_app(Staging)
else:
    app = create_app(Development)


# Before/After request methods
@app.before_request
def load_user():
    g.user = current_user


@app.template_global("current_date")
def current_date():
    from datetime import datetime as dt

    t = dt.now()
    return {"year":t.year, "month":t.month, "day":t.day,
            "hour":t.hour, "minute":t.minute, "second":t.second}


HERE = os.path.abspath(os.path.dirname(__file__))
# TEST_PATH = os.path.join(HERE, 'tests')

manager = Manager(app)


def _make_context():
    """
    Return context dict for a shell session so we can access things
    :return:
    """
    return {'app': app, 'db': db, 'User': User, 'Profile': Profile, 'Template': Template}


manager.add_command('server', Server())
manager.add_command('shell', Shell(make_context=_make_context))
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()