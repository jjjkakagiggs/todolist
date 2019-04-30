# from todolist.extensions import bootstrap,db,migrate,login_manager
from flask import Flask
from todolist.settings import config
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
# from todolist.models import User,Todolist
# from flask_wtf import CSRFProtect


config_name = 'development'
app = Flask('todolist')
app.config.from_object(config[config_name])
bootstrap = Bootstrap(app)
db = SQLAlchemy(app)
login_manager = LoginManager(app)
migrate = Migrate(app,db)
# csrf = CSRFProtect()

@app.shell_context_processor
def make_shell_context():
    from todolist.models import User, Todolist
    return dict(db = db,User = User,Todolist=Todolist)



login_manager.login_view = "login"


from todolist import views