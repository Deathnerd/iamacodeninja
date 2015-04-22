from flask_wtf import Form
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Email, EqualTo, Length


class AccountManagementForm(Form):
	email = StringField('Email', validators=[DataRequired(), Email(), Length(min=6, max=40)])
	active = BooleanField('Account Active')

	def __init__(self, *args, **kwargs):
		super(AccountManagementForm, self).__init__(*args, **kwargs)
		self.user = None

	def validate(self):
		"""
		Validates that the user has all the information needed in their account page
		:return:
		"""
		return super(AccountManagementForm, self).validate()