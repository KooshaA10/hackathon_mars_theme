# app/auth.py
from flask import Blueprint, render_template, redirect, url_for, flash
from byterz.forms import LoginForm, RegisterForm
from byterz.models import User, UserSettings
from byterz import db, login_manager
from flask_login import login_user, logout_user, login_required, current_user

auth_bp = Blueprint("auth", __name__, template_folder="templates")

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("main.index"))
    form = LoginForm()
    if form.validate_on_submit():
        u = User.query.filter_by(username=form.username.data).first()
        if u and u.check_password(form.password.data):
            login_user(u)
            return redirect(url_for("main.index"))
        flash("Invalid credentials", "danger")
    return render_template("login.html", form=form)

@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("main.index"))
    form = RegisterForm()
    if form.validate_on_submit():
        if User.query.filter_by(username=form.username.data).first():
            flash("Username taken", "warning")
        else:
            u = User(username=form.username.data)
            u.set_password(form.password.data)
            db.session.add(u)
            db.session.commit()
            # create default settings
            s = UserSettings(user_id=u.id)
            db.session.add(s)
            db.session.commit()
            flash("Account created. Please log in.", "success")
            return redirect(url_for("auth.login"))
    return render_template("register.html", form=form)

@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("main.index"))