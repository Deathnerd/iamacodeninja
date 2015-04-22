from flask import Blueprint, render_template, g, redirect, url_for, request, flash
from flask.ext.login import login_required
from .forms import AccountManagementForm
from ..models import User, Template, Profile
from ..app import db
from ..utils import flash_errors

blueprint = Blueprint("ninja_user", __name__, url_prefix="/u", static_folder="../static")


@blueprint.route("/<string:user_name>/account", methods=['GET', 'POST'])
@login_required
def manage_user_account(user_name):
	if g.user.username != user_name:
		return redirect(url_for('ninja_user.user_profile', user_name=g.user.username))
	# Handle the changes to a user's account
	user = User.get_by_id(int(g.user.id))
	form = AccountManagementForm(request.form, active=user.active, email=user.email,
								 )
	if request.method == 'POST':
		if form.validate_on_submit():
			user.email = form.email.data
			user.active = form.active.data
			db.session.add(user)
			db.session.commit()
			flash("Account settings saved!", "success")
			return redirect(url_for('ninja_user.manage_user_account', user_name=g.user))
		else:
			flash_errors(form)
	return render_template("user/account.html", user=g.user, form=form)


@blueprint.route('/<string:user_name>')
def user_profile(user_name):
	user = User.query.filter_by(username=user_name).first()
	if not user:
		return "This user does not exist. Have you lost them?"  # Return a 401 page

	template = Template.query.filter_by(id=user.profile.template_id).first()
	return render_template("profile_templates/{}.html".format(template.filename), user=user)