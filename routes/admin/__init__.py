from flask import Blueprint

admin = Blueprint('admin', __name__, url_prefix='/admin')

from . import users,logs  # users.py에서 route 등록
