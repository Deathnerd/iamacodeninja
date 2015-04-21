from flask import Blueprint, render_template, g, redirect, url_for, request
from flask.ext.login import login_required

blueprint = Blueprint("ninja_user", __name__, url_prefix="/u", static_folder="../static")


@blueprint.route("/<string:user_name>/account")
@login_required
def manage_user_account(user_name):
	if g.user.username != user_name:
		return redirect(url_for('ninja_user.user_profile', user_name=g.user.username))
	return "This is the account management page for {user}".format(user=user_name)


@blueprint.route('/<string:user_name>')
def user_profile(user_name):
	return "This is the user page for {user}".format(user=user_name)