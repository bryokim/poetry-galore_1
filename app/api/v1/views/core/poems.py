from flask import abort, jsonify, make_response, request
from flask_login import login_required, fresh_login_required

from app import db
from app.api.v1.views import core_view
from app.models.poem import Poem
from app.models.user import User
from app.models.engine.db_storage import DBStorage


@core_view.route("/poems")
def get_poems():
    """Get all poems.

    Returns:
        list: List of all the poems.
    """
    poems = DBStorage().all(Poem)

    return make_response(
        jsonify([poem.to_dict() for poem in poems.values()]), 200
    )


@core_view.route("/poems/<poem_id>")
def get_poem(poem_id):
    """Get a specific poem.

    Args:
        poem_id (str): The poem id.

    Returns:
        dict: The requested poem.
    """
    poem = DBStorage().get(Poem, poem_id)

    if not poem:
        abort(404)

    return make_response(jsonify(poem.to_dict()), 200)


@core_view.route("/poems", methods=["POST"])
@login_required
def create_poem():
    """Post a poem.

    Returns:
        dict: The newly created poem.
    """
    data = request.get_json(silent=True)

    if not data:
        abort(400, description="Invalid JSON")

    if not data.get("title"):
        abort(400, description="Poem must have title")

    if not data.get("body"):
        abort(400, description="Poem must have body")

    if not data.get("user_id"):
        abort(400, description="Poem must have user_id")

    user = DBStorage().get(User, data.get("user_id"))
    if not user:
        abort(400, description="Invalid user_id")

    new_poem = Poem(**data)

    DBStorage().new(new_poem)
    DBStorage().save()

    return make_response(jsonify(new_poem.to_dict()), 201)


@core_view.route("/poems/<poem_id>", methods=["UPDATE"])
@login_required
def update_poem(poem_id: str):
    """Update a poem.

    Args:
        poem_id (str): The poem id.

    Returns:
        dict: The updated poem.
    """
    data = request.get_json(silent=True)
    poem = DBStorage().get(Poem, poem_id)

    if not poem:
        abort(404)

    if not data:
        abort(400, description="Invalid JSON")

    ignore_keys = ["id", "created_at", "updated_at", "user_id"]
    for key, value in data.items():
        if key not in ignore_keys:
            setattr(poem, key, value)

    DBStorage().new(poem)
    DBStorage().save()

    return make_response(jsonify(poem.to_dict()), 200)


@core_view.route("/poems/<poem_id>", methods=["DELETE"])
@fresh_login_required
def delete_poem(poem_id):
    """Delete a poem.

    Args:
        poem_id (str): The poem id.

    Returns:
        dict: An empty dictionary.
    """
    poem = DBStorage().get(Poem, poem_id)

    if not poem:
        abort(404)

    DBStorage().delete(poem)
    DBStorage().save()

    return make_response(jsonify({}), 200)
