# routes/__init__.py

from .main import main
from .about import about
from .login import login

blueprints = [main, about, login]
