# routes/__init__.py

from .main import main
from .about import about
from .login import login
from .register import register

blueprints = [main, about, login, register]
