
#!/usr/bin/python

import os
from flask import Flask
from flask.ext.babel import Babel
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root@localhost/test'
babel = Babel(app)

db = SQLAlchemy(app)

from jtminer import views
