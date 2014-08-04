"""
Initialize Flask app

"""
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.script import Manager
from flask.ext.migrate import Migrate, MigrateCommand


app = Flask('apps')
db = SQLAlchemy(app)
app.config.from_object('apps.settings.Production')

manager = Manager(app)
migrate = Migrate(app, db)
manager.add_command('db', MigrateCommand)

import controllers, models