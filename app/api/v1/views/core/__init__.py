from flask import jsonify, make_response

from .users import *
from .poems import *
from .poems_likes import *
from app.api.v1.views import core_view


@core_view.errorhandler(404)
def handle_404(error):
    return make_response(jsonify({"error": "Not found"}), 404)


@core_view.errorhandler(400)
def handle_400(error):
    return make_response(jsonify({"error": error.description}), 400)
