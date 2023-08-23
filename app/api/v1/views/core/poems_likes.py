from flask import abort, jsonify, make_response, url_for
from sqlalchemy import text

from app import db
from app.api.v1.views import core_view
from app.models.poem import Poem
from app.models.user import User
from app.models.engine.db_storage import DBStorage


@core_view.route("/poems/<poem_id>/likes", methods=["GET"])
def get_likes(poem_id):
    """Get the number of likes for a poem.

    Args:
        poem_id (str): The poem id.

    Returns:
        dict: A dictionary containing likes and poem id.
    """
    poem = DBStorage().get(Poem, poem_id)

    if not poem:
        abort(404)

    num = len(
        db.session.execute(
            text("SELECT * FROM likes WHERE poem_id=:poem_id").bindparams(
                poem_id=poem_id
            )
        ).all()
    )

    return make_response(jsonify({"likes": num}), 200)


@core_view.route("/poems/<poem_id>/users/<user_id>/likes")
def get_user_likes(poem_id, user_id):
    """Get number of poems user has liked.

    Args:
        poem_id (str): The poem id.
        user_id (str): The user id.

    Returns:
        _type_: _description_
    """
    poem = DBStorage().get(Poem, poem_id)
    user = DBStorage().get(User, user_id)

    if not poem or not user:
        abort(404)

    poem_user_id_tuple_list = db.session.execute(
        text(
            """SELECT * FROM likes
                WHERE poem_id=:poem_id and user_id=:user_id
                """
        ).bindparams(poem_id=poem_id, user_id=user_id)
    ).all()

    return make_response(
        jsonify(
            {
                "likes": len(poem_user_id_tuple_list),
                "poems": [
                    url_for(
                        "core_view.get_poem", poem_id=poem_id, _external=True
                    )
                    for poem_id, _ in poem_user_id_tuple_list
                ],
            }
        ),
        200,
    )


@core_view.route("/poems/<poem_id>/users/<user_id>/like", methods=["POST"])
def like_poem(poem_id, user_id):
    """Post a like for a poem by a user.

    Args:
        poem_id (str): The poem id.
        user_id (str): The user id.

    Returns:
        dict: The user that liked the poem.
    """
    poem = DBStorage().get(Poem, poem_id)
    user = DBStorage().get(User, user_id)

    if not user or not poem:
        abort(404)

    if user not in poem.likes:
        poem.likes.append(user)
        DBStorage().new(poem)
        DBStorage().save()
        return make_response(jsonify(user.to_dict()), 201)
    elif user in poem.likes:
        return make_response(jsonify(user.to_dict()), 200)


@core_view.route("/poems/<poem_id>/users/<user_id>/like", methods=["DELETE"])
def unlike_poem(poem_id, user_id):
    """Delete a like for a poem.

    Args:
        poem_id (str): The poem id.
        user_id (str): The user id.

    Returns:
        dict: An empty dictionary.
    """
    poem = DBStorage().get(Poem, poem_id)
    user = DBStorage().get(User, user_id)

    if not user or not poem or user not in poem.likes:
        abort(404)
    else:
        poem.likes.remove(user)
        DBStorage().new(poem)
        DBStorage().save()

    return make_response(jsonify({}), 200)
