from flask import abort, jsonify, make_response, request
from flask_login import fresh_login_required, login_required

from app.api.v1.views import core_view
from app.models.user import User
from app.models.engine.db_storage import DBStorage


@core_view.route("/users")
def get_users():
    """Get a list of users.

    Returns:
        list: List of all users.
    """
    users = DBStorage().all(User)

    return make_response(jsonify([user.to_dict() for user in users.values()]))


@core_view.route("/users/<user_id>")
@login_required
def get_user(user_id: str):
    """Get a user by user_id.

    Args:
        user_id (str): The user id.

    Returns:
        dict: The requested user.
    """
    user = DBStorage().get(User, user_id)

    if not user:
        abort(404)

    return make_response(jsonify(user.to_dict(password=False)))


@core_view.route("/users", methods=["POST"])
def create_user():
    """Create a new user.

    Returns:
        dict: The newly created user.
    """
    data = request.get_json(silent=True)

    if not data:
        abort(400, description="Invalid JSON")

    if not data.get("username"):
        abort(400, description="Must provide username")

    if not data.get("email"):
        abort(400, description="Must provide email")

    if not data.get("password"):
        abort(400, description="Must provide password")

    new_user = User(**data)

    DBStorage().new(new_user)
    DBStorage().save()

    return make_response(jsonify(new_user.to_dict()), 201)


@core_view.route("/users/<user_id>", methods=["UPDATE"])
@fresh_login_required
def update_user(user_id: str):
    """Update a user.

    Args:
        user_id (str): The user id.

    Returns:
        dict: Newly updated user.
    """
    data = request.get_json(silent=True)
    user = DBStorage().get(User, user_id)

    if not user:
        abort(404)

    if not data:
        abort(400, description="Invalid JSON")

    ignore_keys = ["id", "created_at", "updated_at"]
    for key, value in data.items():
        if key not in ignore_keys:
            setattr(user, key, value)

    DBStorage().new(user)
    DBStorage().save()

    return make_response(jsonify(user.to_dict()), 200)


@core_view.route("/users/<user_id>", methods=["DELETE"])
@fresh_login_required
def delete_user(user_id: str):
    """Delete a user.

    Args:
        user_id (str): The user id.

    Returns:
        dict: An empty dictionary.
    """
    user = DBStorage().get(User, user_id)

    if not user:
        abort(404)

    DBStorage().delete(user)
    DBStorage().save()

    return make_response(jsonify({}), 200)
