from flask import Blueprint, render_template, redirect, url_for
from flask_login import current_user

# Create a blueprint
main = Blueprint("main", __name__)


# Define the root route
@main.route("/")
def home():

    if current_user.is_authenticated:
        return redirect(url_for("dashboard.home"))

    return render_template("index.html")
