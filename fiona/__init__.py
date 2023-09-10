from flask import Flask
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = 'javascript_rules'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///fiona.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 's.panahi.m@gmail.com'
app.config['MAIL_PASSWORD'] = 'slytyjozbhdwlcem'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

app.app_context().push()

db = SQLAlchemy(app)
mail = Mail(app)

from fiona import routes
from fiona import operations
from fiona import admin