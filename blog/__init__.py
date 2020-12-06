from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_marshmallow import Marshmallow

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
app.config['SECRET_KEY'] = 'mysecretkey'
app.config['HOST'] = '0.0.0.0'
db = SQLAlchemy(app)
cors = CORS(app, resources={r"/*": {"origins": "*"}})
login_manager = LoginManager(app)
login_manager.login_view = 'login'

from blog import routes