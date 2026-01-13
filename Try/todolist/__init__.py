from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///todolist.db'
app.config['SECRET_KEY'] = 'e2ce98e51e18d71dcdbcd20f'
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
    "connect_args": {"timeout": 15}  # wait up to 15 seconds for lock release
}


db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'


from todolist import routes 