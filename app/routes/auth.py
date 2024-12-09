from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, current_user
from flask_limiter.util import get_remote_address
from flask_limiter import RateLimitExceeded
from werkzeug.security import generate_password_hash, check_password_hash

from app import db, limiter
from app.forms import RegistrationForm, LoginForm
from app.models.user import User

from app.utils.reset_rate_limit import reset_user_limit

auth = Blueprint("auth", __name__)


# Error handler for rate limits
@auth.errorhandler(RateLimitExceeded)
def handle_rate_limit_exceeded(e):
    flash("Too many attempts. Please try again later.", "danger")
    form = LoginForm()
    return render_template("login.html", form=form), 429


# Login route
@auth.route("/login", methods=["GET", "POST"])
@limiter.limit(
    "5 per hour",
    key_func=get_remote_address,
    error_message="Too many login attempts. Please try again later.",
)
def login():
    form = LoginForm()

    if current_user.is_authenticated:
        return redirect(url_for("dashboard.home"))

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        user = User.query.filter_by(username=username).first()

        if not user or not check_password_hash(user.password, password):
            flash("Invalid username or password.", "danger")
            return render_template("login.html", form=form)

        try:
            reset_user_limit(get_remote_address(), "auth.login")
            login_user(user)
            return redirect(url_for("dashboard.home"))
        except Exception as e:
            print(f"Error logging in {username}: {e}")
            flash(f"Error logging in: {e}", "danger")

    return render_template("login.html", form=form)


# Logout route
@auth.route("/logout")
def logout():
    if not current_user.is_authenticated:
        flash("You are not logged in.", "info")
    else:
        logout_user()
        flash("You have been logged out.", "info")

    return redirect(url_for("auth.login"))


# Registration route
@auth.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("dashboard.home"))

    form = RegistrationForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        confirm_password = form.confirm_password.data

        if password != confirm_password:
            flash("Passwords do not match.", "danger")
            return render_template("register.html", form=form)

        if User.query.filter_by(username=username).first():
            flash("Username already exists.", "danger")
            return render_template("register.html", form=form)

        user = User(username=username, password=generate_password_hash(password))
        db.session.add(user)
        db.session.commit()
        flash("User created successfully.", "success")
        return redirect(url_for("auth.login"))

    return render_template("register.html", form=form)
