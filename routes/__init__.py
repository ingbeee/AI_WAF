from .main import main
from .about import about
from .login import login
from .register import register
from . import admin
from .user import user
blueprints = [main, about, login, register, admin.admin, user]
