from flask import Blueprint, render_template, g, redirect, url_for, request
from flask.ext.login import login_user, logout_user

blueprint = Blueprint("public", __name__, static_folder="../static")


@blueprint.route("/")
def index():
	return "This is the index page"


@blueprint.route('/login')
def login():
	return render_template('public/login.html')


@blueprint.route('/logout')
def logout():
	return render_template('public/logout.html')


@blueprint.route("/register")
def register():
	return "This is the route for the register"