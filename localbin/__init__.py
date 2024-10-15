import os

from dotenv import load_dotenv
from flask import Flask, Response
from flask_migrate import Migrate
from flask_wtf.csrf import CSRFProtect, generate_csrf
from flask_session import Session
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
#import magic
#import pyclamd

"""
Flask init and configuration
"""
# Load env files
load_dotenv('.env.development')

# Init flask app
app = Flask(__name__)

csrf = CSRFProtect()

# Get secret key from .env 
app.secret_key = os.getenv('SECRET_KEY')

#Init login manager for flask_login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth.login'

# Set csrf for app
csrf.init_app(app)

@app.after_request
def add_csrf_cookie(response: Response):
    if response.status_code in range(200, 400) and not response.direct_passthrough:
        response.set_cookie("csrftoken", generate_csrf(), secure=True)
    return response

# Init Session
#sess = Session()

# Configure Session type
app.config['SESSION_TYPE'] = 'filesystem'
#sess.init_app(app)

# Configure the app for db uploads
# Get the absolute path of the current file’s directory
basedir = os.path.abspath(os.path.dirname(__file__))

# Set upload folder
UPLOAD_FOLDER = 'users_space'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Configure allowed files and max size
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'mkv', 'avi', 'eml', 'zip'}

app.config['MAX_CONTENT_LENGTH'] = (1024 * 1024 * 1024) * 1024

#def allowed_mime_type(file):
#    mime = magic.from_buffer(file.stream.read(2048), mime=True)
#    file.stream.seek(0) 
#    return mime in ['image/png', 'image/jpeg', 'application/pdf']

## Scan for malicious code
#def scan_file(file_path):
#    cd = pyclamd.ClamdUnixSocket()
#    result = cd.scan_file(file_path)
#    return result


# Configure the app for db, uploads
# Get the absolute path of the current file’s directory
basedir = os.path.abspath(os.path.dirname(__file__))
db_name = "localbin.db"
app.config['SQLALCHEMY_DATABASE_URI']="sqlite:///" +os.path.join(basedir, db_name)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['WTF_CSRF_UNABLED'] = False
app.config['WTF_CSRF_METHODS'] = []
# Init db and migrate
db = SQLAlchemy(app)
migrate = Migrate(app, db)

app.app_context().push()

# Create db if doesnt exists
if not os.path.isfile(db_name):
    db.create_all()

# Import views
from localbin.auth.models import User
from localbin.events.user_listener import create_home_dir_after_insert

# Import blueprints
from localbin.auth.routes import auth
from localbin.core.routes import core
from localbin.user.routes import user
from localbin.translator.routes import translator  # 你定义的蓝图所在的模块

# Registering blueprints
app.register_blueprint(auth)
app.register_blueprint(core)
app.register_blueprint(user)
app.register_blueprint(translator)  # 注册蓝图

# User loader callback to reload user id stored in session or return None and not raise exception
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
