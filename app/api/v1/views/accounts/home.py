from flask import render_template

from app.api.v1.views import accounts_view


@accounts_view.route("/home")
def home():
    return render_template("accounts/home.html")
