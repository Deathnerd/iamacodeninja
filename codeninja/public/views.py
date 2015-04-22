from flask import Blueprint, render_template, g, redirect, url_for, request, flash
from flask.ext.login import login_user, logout_user, login_required
from .forms import RegisterForm, LoginForm
from ..models import User
from ..utils import flash_errors
from ..extensions import login_manager

blueprint = Blueprint("public", __name__, static_folder="../static")

@login_manager.user_loader
def load_user(id):
	"""
	Provides login_manager with a method to load a user
	"""
	return User.get_by_id(int(id))

@blueprint.route("/")
def index():
	"""
	The public home page. Make it purty and awesome!
	"""
	return "This is the index page"


@blueprint.route('/login', methods=["GET", "POST"])
def login():
	"""
	The all-in-one login page. Handles login logic as well as displaying the page
	:return:
	"""
	# If the user is logged in, then boot them to their account
	if g.user:
		return redirect(url_for('ninja_user.user_profile', user_name=g.user.username))
	form = LoginForm(request.form)
	# Handle the login
	if request.method == 'POST':
		if form.validate_on_submit():
			login_user(form.user)
			flash("You have successfully logged in. Huzzah!", 'success')
			redirect_url = request.args.get("next") or url_for("ninja_user.manage_user_account", user_name=form.user.username)
			return redirect(redirect_url)
		else:
			flash_errors(form)
	return render_template('public/login.html', form=form)


@blueprint.route('/logout')
@login_required
def logout():
	"""
	Handles logout logic
	:return:
	"""
	logout_user()
	return render_template('public/logout.html')


@blueprint.route("/register", methods=['GET', 'POST'])
def register():
	"""
	Handles the register logic as well as displaying the form
	:return:
	"""
	form = RegisterForm(request.form, csrf_enabled=False)
	if form.validate_on_submit():
		new_user = User.create(username=form.username.data,
							   email=form.email.data,
							   password=form.password.data,
							   active=True)
		flash('Thank you for registering. You can now log in!', "success")
		return redirect(url_for('public.index'))
	else:
		flash_errors(form)
	return render_template('public/register.html', form=form)