import os
from dotenv import load_dotenv
from flask import Flask
from flask_wtf.csrf import CSRFProtect

load_dotenv()

app = Flask(__name__)

app.config['SECRET_KEY'] = os.environ['SECRET_KEY']
csrf = CSRFProtect(app)
app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024

from . import views
from .users import users_bp
from .products import products_bp

app.register_blueprint(users_bp)
app.register_blueprint(products_bp)