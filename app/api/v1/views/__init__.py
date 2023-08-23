from flask import Blueprint

accounts_view = Blueprint("accounts_view", __name__)
core_view = Blueprint("core_view", __name__, url_prefix="/api/v1")

from .accounts import *
from .core import *
