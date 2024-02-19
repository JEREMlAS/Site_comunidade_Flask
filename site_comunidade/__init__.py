from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
import sqlalchemy
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'b5801020b88df23191c9bb0d0b73effb'
if os.getenv("DATABASE_URL"):
  app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL")
else:
  app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///comunidade.db'

database = SQLAlchemy(app)
bcrypt = Bcrypt(app)

login_manager = LoginManager(app)
login_manager.login_view = 'cadastro'
login_manager.login_message_category = 'alert-info'

from site_comunidade import models
engine = sqlalchemy.create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
inspector = sqlalchemy.inspect(engine)
if not inspector.has_table("usuario"):
    with app.app_context():
        database.drop_all()
        database.create_all()

from site_comunidade import routes



