from .main import main
from .about import about
from .login import login
from .register import register
from . import admin

blueprints = [main, about, login, register, admin.admin]
